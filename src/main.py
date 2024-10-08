import cv2
import os
from fastapi import FastAPI, UploadFile, Depends, HTTPException, File, Form, Request
from fastapi.responses import FileResponse
from typing import Annotated
from dotenv import dotenv_values, find_dotenv
from sqlalchemy.orm import Session
import schemas 
import crud
from database import Base, engine, get_db
from detector import FaceDetector
from backend_utils import generate_image_metadata, convert_from_string, get_image_from_url
import base64
from json import JSONDecodeError


app = FastAPI()
Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]
accepted_file_type = {"image/jpeg", "image/png"}
config = dotenv_values(find_dotenv())
detector = FaceDetector()
views_path = "./views"

if not os.path.exists(config["IMAGE_STORE_URL"]):
  os.makedirs(config["IMAGE_STORE_URL"])
  print("Create image store directory successfully")

@app.get("/")
def home_page():
  return FileResponse(f"{views_path}/home.html")

@app.get("/find")
def find_page():
  return FileResponse(f"{views_path}/find.html")

@app.post("/find")
async def retrieve_image(db: db_dependency, request: Request):
  content_type = request.headers.get('Content-Type')
  if content_type is None:
    raise HTTPException(status_code=400, detail='No Content-Type provided')
  if content_type != 'application/json':
    raise HTTPException(status_code=400, detail='Content-Type not supported')
  
  try:
    form = await request.json()
  except JSONDecodeError:
    raise HTTPException(status_code=400, detail='Invalid JSON data')
  
  image_id = form["image_id"]
  
  img_information = crud.get_image_information(db, image_id)
  if img_information is None:
    raise HTTPException(status_code=404, detail="Image not found")
  
  img = get_image_from_url(img_information.store_url)
  base64_img = base64.b64encode(img)

  return {"base64_img": base64_img, 
          "person_count": img_information.person_count,
          "img_id": img_information.id}

@app.post("/upload_image")
async def receive_image(db: db_dependency, file: UploadFile= File(...), 
                        confidence: float= Form(default=0.5)):
  if file.content_type not in accepted_file_type:
    raise HTTPException(status_code=422, detail="File is not supported")
  
  content = await file.read()
  img = convert_from_string(content)
  person_count, result_img = detector.detect(img, confidence)
  filename, image_url = generate_image_metadata(file.filename, 
                                                config["IMAGE_STORE_TYPE"],
                                                config["IMAGE_STORE_URL"])
  cv2.imwrite(image_url, result_img)
  image_data = schemas.ImageBase(name= filename, 
                                 store_url= image_url,
                                 person_count= person_count)
  img_information = crud.save_image(db, image_data)
  _, encoded_img = cv2.imencode('.png', result_img)
  base64_img = base64.b64encode(encoded_img)
  return {"base64_img": base64_img, 
          "person_count": img_information.person_count,
          "img_id": img_information.id}
