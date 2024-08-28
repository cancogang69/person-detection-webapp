# Person detection WebApp

A person detection WebApp using:
- FastAPI
- PostgreSQL
- Yolov5

## Installation
- Clone repository: `git clone https://github.com/cancogang69/person-detection-webapp.git`
- Change directory to: `cd person-detection-webapp`
- Install depedencies with: `pip install -r requirements.txt`
- Start PostgreSQL and pgAdmin with docker compose file: `docker compose up -d`
- Change directory to : `cd src`
- Start WebApp server: `uvicorn main:app`
- open http://localhost:8000 and try it out!
