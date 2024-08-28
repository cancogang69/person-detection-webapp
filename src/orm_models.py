from sqlalchemy import Column, String, Integer
from database import Base

class Image(Base):
  __tablename__ = "images"

  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False)
  store_url = Column(String, nullable=False)
  person_count = Column(Integer, nullable=False)