from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union

from model.database import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean, JSON

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
    name = Column(String, nullable=True)
    representation_artist = Column(String, nullable=True)
    artist_list = Column(String, nullable=True)
    album = Column(String, nullable=True)

    def __init__(self, flo) :
        self.id = flo.id
        self.name = flo.name
        self.representation_artist = json.dumps(flo.representationArtist.__dict__)
        self.artist_list = json.dumps([artist.__dict__ for artist in flo.artistList])
        # self.album = json.dumps(flo.album.__dict__)

        # self.representation_artist = flo.representationArtist
        # self.artist_list = flo.artistList
        # self.album = flo.album