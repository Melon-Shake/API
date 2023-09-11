from database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean
from typing import Dict, List, Union

class rankInfo(BaseModel):
     rank:int
     rank_peak:int
     rank_last:int
class GenreModel(BaseModel):
    svc_type:int
    svc_nm:str
class ArtistModel(BaseModel):
    artist_id:int
    artist_nm:str
    genres:List[GenreModel]
class Adhoc_Attr(BaseModel):
    likes_count:int
class ImageInfo(BaseModel):
    path:str
class Albuminfo(BaseModel):
     album_id: int
     title: str
     image:ImageInfo
     release_ymd : str
     release_local_ymd : str


class BugsEntity(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    track_id: int
    track_title: str
    album: Albuminfo
    artists: List[ArtistModel]
    adhoc_attr: Adhoc_Attr
    list_attr:rankInfo

class Bugs_Load(BaseModel) :
    vibe: List[BugsEntity]
