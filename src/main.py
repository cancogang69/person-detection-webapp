import cv2
from fastapi import FastAPI, UploadFile, File
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def home():
  return {"message": "welcome"}




