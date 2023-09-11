from model.database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean
from typing import Dict, List, Union

from model.database import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean, JSON, DateTime, Float
from sqlalchemy.sql import func

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

class BugsORM(Base) :
    __tablename__ = 'chart_bugs'

    id = Column(Integer, primary_key=True)
    track_id = Column(Integer, nullable=True)
    track_title = Column(String, nullable=True)
    album_id = Column(Integer, nullable=True)
    album_title = Column(String, nullable=True)
    album_image_path = Column(String, nullable=True)
    album_release_ymd = Column(String, nullable=True)
    album_release_local_ymd = Column(String, nullable=True)
    artist_id = Column(Integer, nullable=True)
    artist_name = Column(String, nullable=True) 
    genres_name = Column(String, nullable=True) 
    likes_count = Column(Integer, nullable=True)
    rank = Column(Integer, nullable=True)
    rank_peak = Column(Integer, nullable=True)
    rank_last = Column(Integer, nullable=True)
    points = Column(Float, nullable=True)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self,entity) :
        self.track_id = entity.track_id
        self.track_title = entity.track_title
        self.album_id = entity.album.album_id
        self.album_title = entity.album.title
        self.album_image_path = 'https://image.bugsm.co.kr/album/images/256'+entity.album.image.path
        self.album_release_ymd = entity.album.release_ymd
        self.album_release_local_ymd = entity.album.release_local_ymd
        self.artist_id = entity.artists[0].artist_id
        self.artist_name = entity.artists[0].artist_nm
        self.genres_name = entity.artists[0].genres[0].svc_nm
        self.likes_count = entity.adhoc_attr.likes_count
        self.rank = entity.list_attr.rank
        self.rank_peak = entity.list_attr.rank_peak
        self.rank_last = entity.list_attr.rank_last
        self.points = (101-self.rank)*3.1