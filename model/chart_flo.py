from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union

from model.database import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean

class RepresentationArtist(BaseModel):
    id: int
    name:str

class Album(BaseModel):
    id: int
    imgList:List[Dict[str,Union[str,int]]]
    title: str
    releaseYmd : str

class ChartFlo(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    representationArtist: RepresentationArtist
    artistList: List[Dict[str,Union[str,int]]]
    album: Album