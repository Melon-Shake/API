from urllib.parse import unquote
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Dict, List, Union

from model.database import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Integer, ARRAY, Float, DateTime
from sqlalchemy.sql import func

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

class ChartGenieORM(Base) :
    __tablename__ = 'chart_genie'

    id = Column(Integer, primary_key=True)
    track_name = Column(String, nullable=True)
    track_id = Column(String, nullable=True)
    artist_names = Column(String, nullable=True)
    artist_ids = Column(ARRAY(String), nullable=True)
    album_name = Column(String, nullable=True)
    album_id = Column(String, nullable=True)
    img_url = Column(String, nullable=True)
    rank_no = Column(Integer, nullable=True)
    pre_rank_no = Column(Integer, nullable=True)
    points = Column(Float, nullable=True)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, genie:ChartGenie) :
        self.track_name = genie.SONG_NAME
        self.artist_names = genie.ARTIST_NAME
        self.album_name = genie.ALBUM_NAME
        self.img_url = genie.ALBUM_IMG_PATH
        self.rank_no = int(genie.RANK_NO)
        self.pre_rank_no = int(genie.PRE_RANK_NO)
        self.points = (101-self.rank_no)*9.2