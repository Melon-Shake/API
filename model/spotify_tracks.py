import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column
from sqlalchemy import String

class SpotifyTracks(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    id: str

class SpotifyTracksORM(Base) :
    __tablename__ = 'spotify_tracks'

    id = Column(String, primary_key=True)

    def __init__(self, tracks) :
        pass