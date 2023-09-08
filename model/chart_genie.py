from urllib.parse import unquote
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Dict, List, Union

from model.database import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Integer, ARRAY, Float, DateTime
from sqlalchemy.sql import func

class ChartGenieORM(Base) :
    __tablename__ = 'chart_genie'

    song_id = Column(String, primary_key=True)
    song_name = Column(String, nullable=True)
    artist_id = Column(String, nullable=True)
    artist_name = Column(String, nullable=True)
    album_id = Column(String, nullable=True)
    album_name = Column(String, nullable=True)
    album_img_path = Column(String, nullable=True)
    rank_no = Column(String, nullable=True)
    pre_rank_no = Column(String, nullable=True)
    points = Column(Float, nullable=True)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, genie) :
        self.song_id = int(genie.SONG_ID)
        self.song_name = genie.SONG_NAME
        self.artist_id = int(genie.ARTIST_ID)
        self.artist_name = genie.ARTIST_NAME
        self.album_id = int(genie.ALBUM_ID)
        self.album_name = genie.ALBUM_NAME
        self.album_img_path = genie.ALBUM_IMG_PATH
        self.rank_no = int(genie.RANK_NO)
        self.pre_rank_no = int(genie.PRE_RANK_NO)
        self.points = (101-self.rank_no)*9.2

class ChartGenie(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    SONG_ID: str
    SONG_NAME: str
    ARTIST_ID: str
    ARTIST_NAME: str
    ALBUM_ID: str
    ALBUM_NAME: str
    ALBUM_IMG_PATH: str
    RANK_NO: str
    PRE_RANK_NO: str

    @field_validator('SONG_NAME', 'ARTIST_NAME', 'ALBUM_NAME', 'ALBUM_IMG_PATH')
    @classmethod
    def decode_url(cls, v):
        return unquote(v)