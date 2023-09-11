import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union, Optional
from model.database import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Integer, ARRAY


class Images(BaseModel):
    url: str
class Followers(BaseModel) :
    total: Optional[int]
class ExternalUrls(BaseModel):
    spotify: str

class SpotifyArtists(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    external_urls: ExternalUrls
    followers: Followers
    genres: List[str]
    href: str
    id: str
    images: List[Images]
    name: str
    popularity: int
    uri: str

class SpotifyArtistsORM(Base) :
    __tablename__ = 'spotify_artists'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    uri = Column(String, nullable=True)
    href = Column(String, nullable=True)
    external_urls = Column(String, nullable=True)
    images_url = Column(String, nullable=True)
    popularity = Column(Integer, nullable=True)
    followers_total = Column(Integer, nullable=True)
    genres = Column(ARRAY(String))

    def __init__(self,artists:SpotifyArtists):
        self.id = artists.id
        self.name = artists.name
        self.uri = artists.uri
        self.href = artists.href
        self.external_urls = artists.external_urls.spotify
        self.images_url = artists.images[0].url
        self.popularity = artists.popularity
        self.followers_total = artists.followers.total
        self.genres = artists.genres