import string
import random
import cv2
import numpy as np

image_type = {".jpg", ".png"}

def convert_from_string(string):
  nparr = np.fromstring(string, np.uint8)
  img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
  return img

def id_generator(size= 6, chars= string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def remove_filetype(filename):
  if filename[-4:] in image_type:
    filename = filename[:-4]
  
  return filename

def generate_image_metadata(filename, filetype, store_url):
  filename = remove_filetype(filename)
  random_id = id_generator()
  processed_filename = f"{filename}_{random_id}.{filetype}"
  image_url = f"{store_url}/{processed_filename}"

  return processed_filename, image_url