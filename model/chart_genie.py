from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union

class ChartGenie(BaseModel) :
    SONG_ID: str
    SONG_NAME: str