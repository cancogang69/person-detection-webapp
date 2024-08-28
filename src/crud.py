from sqlalchemy.orm import Session
import orm_models 
import schemas

def save_image(db: Session, image: schemas.ImageBase):
  db_image = orm_models.Image(name= image.name, 
                              store_url = image.store_url, 
                              person_count= image.person_count)
  db.add(db_image)
  db.commit()
  db.refresh(db_image)
  return db_image

def get_image_information(db: Session, image_id: int):
  return db.query(orm_models.Image).filter(orm_models.Image.id == image_id).first()