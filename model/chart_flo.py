from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union

from model.database import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean, JSON, DateTime
from sqlalchemy.sql import func

import json

class Img(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    url: str

class Album(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    imgList:List[Img]
    title: str
    releaseYmd : str

class Artist(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

class RepresentationArtist(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name:str

class ChartFlo(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    representationArtist: RepresentationArtist
    artistList: List[Artist]
    album: Album

class ChartFloORM(Base) :
    __tablename__ = 'chart_flo'

    id = Column(Integer, primary_key=True)
    track_id = Column(Integer, nullable=True)
    track_name = Column(String, nullable=True)
    artist_id = Column(Integer, nullable=True)
    artist_name = Column(String, nullable=True)
    album_id = Column(Integer, nullable=True)
    album_name = Column(String, nullable=True)
    img_url = Column(String, nullable=True)
    release_ymd = Column(String, nullable=True)
    rank = Column(Integer, nullable=True)
    points = Column(Integer, nullable=True)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, idx, entity: ChartFlo) :
        self.track_id = entity.id
        self.track_name = entity.name
        self.artist_id = entity.representationArtist.id
        self.artist_name = entity.representationArtist.name
        self.album_id = entity.album.id
        self.album_name = entity.album.title
        self.img_url = entity.album.imgList[0].url
        self.release_ymd = entity.album.releaseYmd
        self.rank = idx+1
        self.points = (100-idx)*6.1