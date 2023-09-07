from model.database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean
from typing import Dict, List, Union

class RepresentationArtistInfo(BaseModel):
    id: int
    name:str

class Albuminfo(BaseModel):
    id: int
    imgList:List[Dict[str,Union[str,int]]]
    title: str
    releaseYmd : str

class FloEntity(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    representationArtist: RepresentationArtistInfo
    artistList: List[Dict[str,Union[str,int]]]
    album: Albuminfo

class Flo_Load(BaseModel) :
    flo: List[FloEntity]