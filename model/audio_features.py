import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.database import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Integer, ARRAY
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union, Optional

class SpotifyAudioFeatures(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    acousticness: float
    danceability: float
    energy: float
    instrumentalness: float
    liveness: float
    loudness: float
    speechiness: float
    tempo: float
    valence: float

class SpotifyAudioFeaturesORM(Base):
    __tablename__ = 'spotify_audio_features'

    id = Column(String, primary_key=True)

    def __init__(self, audio_features:SpotifyAudioFeatures) :
        self.id = audio_features.id