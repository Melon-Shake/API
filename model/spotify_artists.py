from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union
from model.database import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Integer, ARRAY

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

    def __init__(self,artists):
        # self.id = artists.get('id')
        # self.name = artists.get('name')
        # self.uri = artists.get('uri')
        # self.href = artists.get('href')
        # self.external_urls = artists.get('external_urls').get('spotify')
        # self.images_url = artists.get('images')[0].get('url')
        # self.popularity = artists.get('popularity')
        # self.followers_total = artists.get('followers').get('total')
        # self.genres = artists.get('genres')
        self.id = artists.id
        self.name = artists.name
        self.uri = artists.uri
        self.href = artists.href
        self.external_urls = artists.external_urls.get('spotify')
        self.images_url = artists.images[0].get('url')
        self.popularity = artists.popularity
        self.followers_total = artists.followers.get('total')
        self.genres = artists.genres

class SpotifyArtists(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    external_urls: Dict[str,str]
    followers: Dict[str,Union[int,None]]
    genres: List[str]
    href: str
    id: str
    images: List[Dict[str,Union[int,str]]]
    name: str
    popularity: int
    uri: str