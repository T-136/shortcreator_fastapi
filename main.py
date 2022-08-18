from fastapi import FastAPI, Depends, Request, File, Response
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse

from io import BytesIO
import os

from sql_db.database import SessionLocal, engine
from sql_db import crud
from sql_db import models
# from sql_db.database import Base

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000/",
    "http://127.0.0.1:8000/create_new_clip"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

videoFolder = "/home/tilman/Desktop/streetviewvideotest/"

# Dependency
def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/create_new_clip")
def create_new_clip(db: Session = Depends(get_db)):
    return crud.create_clip(db)

@app.get("/showall")
async def read_item(db: Session = Depends(get_db)):
    clip_object_list = crud.get_allclips(db, limit=100, skip=0)

    return clip_object_list

@app.get("/edit/{clip_id}")
async def edit(clip_id: int, db: Session = Depends(get_db)):
    clip_dict = crud.get_clip(db, clip_id)
    return clip_dict

@app.post("/write_edit/")
async def write_edit(request: Request, db: Session = Depends(get_db)):
    clip_dict = await request.json()
    print(clip_dict)
    crud.write_edit_db(clip_dict, db)
    return "success"

@app.post("/sendStreetviewVideo")
async def sendStreetviewVideo(request: Request = File(), db: Session = Depends(get_db)):
    clip_id = int(request.headers["content-disposition"])
    file = await request.body()
    b = BytesIO(file)

    crud.storeStreetviewVideo(clip_id, b, videoFolder)
    crud.writeStreetviewVideoPath(clip_id, videoFolder , db)

    return "uploaded video"

@app.get("/getStreetviewVideo/{clip_id}.mp4")
async def getStreetviewVideo(clip_id): 
    
    filename = videoFolder + "/streetviewvideo-" + str(clip_id)
    if os.path.exists(filename):
        return FileResponse(filename, media_type="video/mp4")
    elif not os.path.exists(filename): 
        return None

@app.get("/delete/{clip_id}")
def delete(clip_id: int, db: Session = Depends(get_db)):
    crud.delete_from_db(clip_id, db)
    crud.delete_video(clip_id, videoFolder)
    return f'deleted clip id: {clip_id}'


