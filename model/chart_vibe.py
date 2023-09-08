from model.database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean
from typing import Dict, List, Union

class rankInfo(BaseModel):
    currentRank:int

class Albuminfo(BaseModel):
    albumId: int
    albumTitle: str
    releaseDate : str
    imageUrl:str

class VibeEntity(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    trackId: int
    trackTitle: str
    artists: List[Dict[str,Union[str,int]]]
    # artistList: List[Dict[str,Union[str,int]]]
    album: Albuminfo
    rank:rankInfo

class Vibe_Load(BaseModel) :
    vibe: List[VibeEntity]