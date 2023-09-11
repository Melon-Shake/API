import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Integer

class ExternalUrls(BaseModel):
    spotify: str
class SpotifyTracks(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    uri: str
    href: str
    external_urls: ExternalUrls
    popularity: int
    track_number: int
    disc_number: int
    duration_ms: int

class SpotifyTracksORM(Base) :
    __tablename__ = 'spotify_tracks'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    uri = Column(String, nullable=True)
    href = Column(String, nullable=True)
    external_urls = Column(String, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    popularity = Column(Integer, nullable=True)
    disc_number = Column(Integer, nullable=True)
    track_number = Column(Integer, nullable=True)

    def __init__(self, tracks:SpotifyTracks) :
        self.id = tracks.id
        self.name = tracks.name
        self.uri = tracks.uri
        self.href = tracks.href
        self.external_urls = tracks.external_urls.spotify
        self.duration_ms = tracks.duration_ms
        self.popularity = tracks.popularity
        self.disc_number = tracks.disc_number
        self.track_number = tracks.track_number