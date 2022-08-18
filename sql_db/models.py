from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary 
from sqlalchemy.orm import relationship

from .database import Base

class Clip(Base):
    __tablename__ = "clip"

    clip_id = Column(Integer, primary_key=True)
    gMapsLink = Column(String, default="")
    name = Column(String, default="")
    group = Column(String, default="")
    videotext = Column(String, default="")
    latlong = Column(String, default="")
    start = Column(Integer, default=0)
    stop = Column(Integer, default=0)
    streetviewVideo = Column(String)
    isRenderd = Column(Boolean, default=False)
    isUploadedYt = Column(Boolean, default=False)
    isUploadedTikTok = Column(Boolean, default=False)
    isUploadedInstagram = Column(Boolean, default=False)

    ymusic_id = Column(Integer, ForeignKey("ymusic.ymusic_id"))
    ymusic = relationship("Ymusic", back_populates="clip")


class Ymusic(Base):
    __tablename__ = "ymusic"

    ymusic_id = Column(Integer, primary_key = True)
    title = Column(String)

    clip = relationship('Clip', back_populates = 'ymusic') 
