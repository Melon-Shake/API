import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.database import Base
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union, Optional
from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Integer, ARRAY

class Images(BaseModel) :
    url: str
class ExternalUrls(BaseModel):
    spotify: str

class SpotifyAlbums(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    uri: str
    href: str
    external_urls: ExternalUrls
    images: List[Images]
    album_type: str
    total_tracks: int
    release_date: str
    release_date_precision: str

class SpotifyAlbumsORM(Base) :
    __tablename__ = 'spotify_albums'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    uri = Column(String, nullable=True)
    href = Column(String, nullable=True)
    external_urls = Column(String, nullable=True)
    images_url = Column(String, nullable=True)
    album_type = Column(String, nullable=True)
    total_tracks = Column(Integer, nullable=True)
    release_date = Column(String, nullable=True)
    release_date_precision = Column(String, nullable=True)

    def __init__(self, albums:SpotifyAlbums) :
        self.id = albums.id
        self.name = albums.name
        self.uri = albums.uri
        self.href = albums.href
        self.external_urls = albums.external_urls.spotify
        self.images_url = albums.images[0].url
        self.album_type = albums.album_type
        self.total_tracks = albums.total_tracks
        self.release_date = albums.release_date
        self.release_date_precision = albums.release_date_precision