import cv2
import numpy as np
import torch

class FaceDetector():
  def __init__(self, 
               model_path= "ultralytics/yolov5",
               model_type= "yolov5s",
               threshold= 0.5,
               bbox_thickness= 2,
               bbox_color= (255, 0, 0)):
    self.model = torch.hub.load(model_path, model_type, _verbose=False)
    self.threshold = threshold
    self.bbox_thickness = bbox_thickness
    self.bbox_color = bbox_color

  def detect(self, img):
    results = self.model(img)
    
    result_df = results.pandas().xyxy[0]
    person_df = result_df[result_df["name"] == "person"]
    person_df = person_df[person_df["confidence"] >= self.threshold]
    person_bboxes = person_df.iloc[:, :4].values

    for person_bbox in person_bboxes:
      start_point = (int(person_bbox[0]), int(person_bbox[1]))
      end_point = (int(person_bbox[2]), int(person_bbox[3]))
      cv2.rectangle(img, start_point, end_point, 
                            self.bbox_color, self.bbox_thickness)

    return len(person_bboxes), img