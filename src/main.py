import cv2
import os
import numpy as np
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import Response
from typing import Annotated
from dotenv import dotenv_values, find_dotenv
from sqlalchemy.orm import Session
import orm_models
import schemas 
import crud
from database import Base, engine, SessionLocal, get_db
from detector import FaceDetector
from backend_utils import generate_image_metadata, convert_from_string
import time


app = FastAPI()
Base.metadata.create_all(bind=engine)
db_dependency = Annotated[Session, Depends(get_db)]
accepted_file_type = {"image/jpeg", "image/png"}
config = dotenv_values(find_dotenv())
detector = FaceDetector(threshold= float(config["FACE_DETECT_THRESHOLD"]))

if not os.path.exists(config["IMAGE_STORE_URL"]):
  os.makedirs(config["IMAGE_STORE_URL"])
  print("Create image store directory successfully")

@app.get("/")
def home():
  return {"message": "welcome"}

@app.post("/upload_image", response_model= schemas.Image)
async def receive_image(file: UploadFile, db: db_dependency):
  if file.content_type not in accepted_file_type:
    raise HTTPException(status_code=422, detail="File is not supported")
  
  content = await file.read()
  img = convert_from_string(content)
  person_count, img = detector.detect(img)
  filename, image_url = generate_image_metadata(file.filename, 
                                                config["IMAGE_STORE_TYPE"],
                                                config["IMAGE_STORE_URL"])
  cv2.imwrite(image_url, img)
  image_data = schemas.ImageBase(name= filename, 
                                 store_url= image_url,
                                 person_count= person_count)
  return crud.save_image(db, image_data)
