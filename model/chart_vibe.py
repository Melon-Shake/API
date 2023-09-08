from model.database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean, Float
from typing import Dict, List, Union

from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean, JSON, DateTime
from sqlalchemy.sql import func

class rankInfo(BaseModel):
    currentRank:int

class Albuminfo(BaseModel):
    albumId: int
    albumTitle: str
    releaseDate : str
    imageUrl:str
    albumGenres: str

class ArtistInfo(BaseModel):
    artistId: int
    artistName: str

class VibeEntity(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    trackId: int
    trackTitle: str
    artists: List[ArtistInfo]
    # artists: List[Dict[str,Union[str,int]]]
    # artistList: List[Dict[str,Union[str,int]]]
    album: Albuminfo
    rank:rankInfo

class Vibe_Load(BaseModel) :
    vibe: List[VibeEntity]

class VibeORM(Base):
    __tablename__ = 'chart_vibe'

    id = Column(Integer, primary_key=True)
    track_id = Column(Integer, nullable=True)
    track_title = Column(String, nullable=True)
    artist_id = Column(Integer, nullable=True)
    artist_name = Column(String, nullable=True)
    album_id = Column(Integer, nullable=True)
    album_title = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    release_date = Column(String, nullable=True)
    album_genres = Column(String, nullable=True)
    current_rank = Column(Integer, nullable=True)
    points = Column(Float, nullable=True)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, entity) :
        self.track_id = entity.trackId
        self.track_title = entity.trackTitle
        self.artist_id = entity.artists[0].artistId
        self.artist_name = entity.artists[0].artistName
        self.album_id = entity.album.albumId
        self.album_title = entity.album.albumTitle
        self.image_url = entity.album.imageUrl
        self.release_date = entity.album.releaseDate
        self.album_genres = entity.album.albumGenres
        self.current_rank = entity.rank.currentRank
        self.points = (101-self.current_rank)*3.6