from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union

from model.database import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Integer, ARRAY

class ChartGenieORM(Base) :
    __tablename__ = 'genie_chart'

    song_id = Column(String, primary_key=True)
    song_name = Column(String, nullable=True)
    artist_id = Column(String, nullable=True)
    artist_name = Column(String, nullable=True)
    album_id = Column(String, nullable=True)
    album_name = Column(String, nullable=True)
    album_img_path = Column(String, nullable=True)
    rank_no = Column(String, nullable=True)
    pre_rank_no = Column(String, nullable=True)

    def __init__(self, genie) :
        self.song_id = genie.SONG_ID
        self.song_name = genie.SONG_NAME
        self.artist_id = genie.ARTIST_ID
        self.artist_name = genie.ARTIST_NAME
        self.album_id = genie.ALBUM_ID
        self.album_name = genie.ALBUM_NAME
        self.album_img_path = genie.ALBUM_IMG_PATH
        self.rank_no = genie.RANK_NO
        self.pre_rank_no = genie.PRE_RANK_NO

class ChartGenie(BaseModel) :
    SONG_ID: str
    SONG_NAME: str
    ARTIST_ID: str
    ARTIST_NAME: str
    ALBUM_ID: str
    ALBUM_NAME: str
    ALBUM_IMG_PATH: str
    RANK_NO: str
    PRE_RANK_NO: str