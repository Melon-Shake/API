from model.database import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Integer, ARRAY, Float
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union, Optional

class AudioFeatures(BaseModel):
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

class AudioFeaturesORM(Base):
    __tablename__ = 'spotify_audio_features'

    id = Column(String, primary_key=True)
    acousticness = Column(Float, default=0)
    danceability = Column(Float, default=0)
    energy = Column(Float, default=0)
    instrumentalness = Column(Float, default=0)
    liveness = Column(Float, default=0)
    loudness = Column(Float, default=0)
    speechiness = Column(Float, default=0)
    tempo = Column(Float, default=0)
    valence = Column(Float, default=0)

    def __init__(self, audio:AudioFeatures) :
        self.id = audio.id
        self.acousticness = audio.acousticness
        self.danceability = audio.danceability
        self.energy = audio.energy
        self.instrumentalness = audio.instrumentalness
        self.liveness = audio.liveness
        self.loudness = audio.loudness
        self.speechiness = audio.speechiness
        self.tempo = audio.tempo
        self.valence = audio.valence