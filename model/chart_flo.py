from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union

from model.database import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean, JSON

class Album(BaseModel):
    id: int
    imgList:List[Dict[str,Union[str,int]]]
    title: str
    releaseYmd : str

class Artist(BaseModel) :
    id: int
    name: str

class RepresentationArtist(BaseModel):
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
    representation_artist = Column(JSON, nullable=True)
    artist_list = Column(JSON, nullable=True)
    album = Column(JSON, nullable=True)

    def __init__(self, flo) :
        self.id = flo.id
        self.name = flo.name
        self.representation_artist = flo.representationArtist
        self.artist_list = flo.artistList
        self.album = flo.album