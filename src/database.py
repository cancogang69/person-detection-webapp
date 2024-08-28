from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values, find_dotenv

config = dotenv_values(find_dotenv())

engine = create_engine(config["POSTGRES_DB_URL"])

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()