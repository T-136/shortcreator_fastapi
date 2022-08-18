from sqlalchemy.orm import Session
import psycopg2
from io import BytesIO
import os

from  sql_db import models
# from sql_db import schemas

def get_clip(db: Session, clip_id: int):
    return db.query(models.Clip).filter(models.Clip.clip_id == clip_id).first()

def get_allclips(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Clip).limit(limit).all()

def get_ymusic(db: Session, ymusic_id: str):
    return db.query(models.Ymusic).filter(models.Ymusic.ymusic_id == ymusic_id).first()

def get_allymusic(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ymusic).offset(skip).limit(limit).all()

def create_clip(db: Session):
    db_clip = models.Clip()
    db.add(db_clip)
    db.commit()
    db.refresh(db_clip)
    return db_clip

def create_ymusic(db: Session):
    db_ymusic = models.Ymusic()
    db.add(db_ymusic)
    db.commit()
    db.refresh(db_ymusic)
    return db_ymusic

def edit_clip(db: Session, data_for_clip):
    clip = db.query(models.Clip).filter(models.Clip.clip_id == clip.clip_id).first()
    clip = edit_clip(clip, data_for_clip)
    return clip
    
def write_edit_db(data_for_clip, db: Session):
    clip, ymusic, nameOfExistingSong = addDataToClip(data_for_clip, db)
    db.add(clip)
    db.commit()
    db.refresh(clip)
    return clip, ymusic, nameOfExistingSong

def addDataToClip(requestform, db: Session):
    print(requestform)
    
    # create latlong if not given but gmapsLink exists
    try:
        if requestform["latlong"] == "" and requestform["gMapsLink"] != "":
            requestform["latlong"] = ",".join(requestform["gMapsLink"].split("@")[1].split(",")[0:2])
    except: 
        print("could not create latlong, is the gmapsLink correct?")

    clip = db.query(models.Clip).filter(models.Clip.clip_id == requestform["clip_id"]).first() 


    # find or create Ymusic
    if (requestform["ymusic_id"] != "" and requestform["ymusic_id"] != None and requestform["ymusic_id"] != "None"):

        if  db.query(models.Ymusic).filter(models.Ymusic.ymusic_id == requestform["ymusic_id"]).first():
            ymusic = db.query(models.Ymusic).filter(models.Ymusic.ymusic_id == requestform["ymusic_id"]).first()
            nameOfExistingSong = ymusic.title
        
        elif not (models.Ymusic.query.filter_by(ymusic_id=requestform["ymusic_id"]).first()):
            ymusic = models.Ymusic()
            nameOfExistingSong = ""
    else:
        ymusic = None
        nameOfExistingSong = ""

    # set boulean if not in request
    for checkboxe in  ['isRenderd', 'isUploadedInst', 'isUploadedYt', 'isUploadedTikTok']:
        if checkboxe not in requestform:
            setattr(clip, checkboxe, 0)

    
    for request_iteration in requestform:
        if request_iteration == "clip_id":
            continue

        if requestform[request_iteration] == "on":
            setattr(clip, request_iteration, 1) 
        elif requestform[request_iteration] == "non":
            setattr(clip, request_iteration, 0)

        elif request_iteration == "ymusic_id" or request_iteration == "title":
            if ymusic != None:
                setattr(ymusic, request_iteration, requestform[request_iteration])
         
        elif request_iteration in ["start", "stop"] and (requestform[request_iteration] == "" or requestform[request_iteration] == "None"):
            setattr(clip, request_iteration, None)
        else:
            setattr(clip, request_iteration, requestform[request_iteration])


    return clip, ymusic, nameOfExistingSong 


def delete_from_db(clip_id, db: Session):
    db.delete(db.query(models.Clip).filter(models.Clip.clip_id == clip_id).first())
    db.commit()

def delete_video(clip_id, videoFolder):
    filename = videoFolder + "/streetviewvideo-" + str(clip_id)
    os.remove(filename)
    

def storeStreetviewVideo(clip_id, video: BytesIO, videoFolder):
    filename = videoFolder + "/streetviewvideo-" + str(clip_id)
    with open(filename, "wb") as f:
        f.write(video.getbuffer())

def writeStreetviewVideoPath(clip_id, videoFolder,  db: Session):
    clip = db.query(models.Clip).filter(models.Clip.clip_id == clip_id).first()
    setattr(clip,  "streetviewVideo", videoFolder)
    db.commit()

def get_streetviewVideo(clip_id, videoFolder):

    filename = videoFolder + "/streetviewvideo-" + str(clip_id)
    with open(filename, "rb") as f:
        yield f.read()

def requestvideo(clip_id, db: Session):
    clip = db.query(models.Clip).filter(models.Clip.clip_id == clip_id).first()
    