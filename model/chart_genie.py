from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union

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