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