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

class Vibe_Load(BaseModel) :
    tracks: List[VibeEntity]

class VibeORM(Base):
    __tablename__ = 'chart_vibe'

    id = Column(Integer, primary_key=True)
    # track_id = Column(Integer, nullable=True)
    track_title = Column(String, nullable=True)
    # artist_ids = Column(ARRAY(Integer), nullable=True)
    artist_names = Column(ARRAY(String), nullable=True)
    # album_id = Column(Integer, nullable=True)
    album_title = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    release_date = Column(String, nullable=True)
    album_genres = Column(String, nullable=True)
    current_rank = Column(Integer, nullable=True)
    points = Column(Float, nullable=True)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, entity) :
        self.track_title = entity.trackTitle
        self.artist_names = list()
        self.album_title = entity.album.albumTitle
        self.image_url = entity.album.imageUrl
        self.release_date = entity.album.releaseDate
        self.album_genres = entity.album.albumGenres
        self.current_rank = entity.rank.currentRank
        self.points = (101-self.current_rank)*3.6