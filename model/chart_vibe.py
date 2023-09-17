from model.database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean, Float
from typing import Dict, List, Union, Optional

from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean, JSON, DateTime, ARRAY
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
    artistName: Optional[str]

class VibeEntity(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    trackId: int
    trackTitle: str
    artists: List[ArtistInfo]
    album: Albuminfo
    rank:rankInfo

class ChartVibe(BaseModel) :
    tracks: List[VibeEntity]

class VibeORM(Base):
    __tablename__ = 'chart_vibe'

    id = Column(Integer, primary_key=True)
    track_id = Column(Integer, nullable=True)
    track_name = Column(String, nullable=True)
    artist_ids = Column(ARRAY(String), nullable=True)
    artist_names = Column(String, nullable=True)
    album_id = Column(Integer, nullable=True)
    album_name = Column(String, nullable=True)
    img_url = Column(String, nullable=True)
    release_date = Column(String, nullable=True)
    album_genres = Column(String, nullable=True)
    current_rank = Column(Integer, nullable=True)
    points = Column(Float, nullable=True)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, entity) :
        self.track_name = entity.trackTitle
        self.artist_names = entity.artists
        self.album_name = entity.album.albumTitle
        self.img_url = entity.album.imageUrl
        self.release_date = entity.album.releaseDate
        self.album_genres = entity.album.albumGenres
        self.current_rank = entity.rank.currentRank
        self.points = (101-self.current_rank)*3.6