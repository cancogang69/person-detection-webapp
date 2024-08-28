from pydantic import BaseModel

class ImageBase(BaseModel):
  name: str
  store_url: str
  person_count: int

class Image(ImageBase):
  id: int

  class Config:
    orm_mode = True