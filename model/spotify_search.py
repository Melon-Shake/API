import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
from model.database import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Integer, ARRAY
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union, Optional

class Images(BaseModel):
    url: str

class ExternalUrls(BaseModel):
    spotify: str

class Followers(BaseModel) :
    total: Optional[int]

class Artists(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    external_urls: ExternalUrls
    # followers: Followers
    # genres: List[str]
    href: str
    id: str
    # images: List[Images]
    name: str
    # popularity: int
    uri: str

class ArtistsORM(Base) :
    __tablename__ = 'spotify_artists'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    uri = Column(String, nullable=True)
    href = Column(String, nullable=True)
    external_urls = Column(String, nullable=True)
    images_url = Column(String, nullable=True)
    popularity = Column(Integer, nullable=True)
    followers_total = Column(Integer, nullable=True)
    genres = Column(String, nullable=True)

    def __init__(self,artists:Artists):
        self.id = artists.id
        self.name = artists.name
        self.uri = artists.uri
        self.href = artists.href
        self.external_urls = artists.external_urls.spotify
        self.images_url = artists.images[0].url
        self.popularity = artists.popularity
        self.followers_total = artists.followers.total
        self.genres = artists.genres

class Albums(BaseModel) :
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
    artists: List[Artists]

class AlbumsORM(Base) :
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

    def __init__(self, albums:Albums) :
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

class Tracks(BaseModel) :
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
    artists: List[Artists]
    album: Albums

class TracksORM(Base) :
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
    artists_ids = Column(ARRAY(String), nullable=True)
    album_id = Column(String, nullable=True)

    def __init__(self, tracks:Tracks) :
        self.id = tracks.id
        self.name = tracks.name
        self.uri = tracks.uri
        self.href = tracks.href
        self.external_urls = tracks.external_urls.spotify
        self.duration_ms = tracks.duration_ms
        self.popularity = tracks.popularity
        self.disc_number = tracks.disc_number
        self.track_number = tracks.track_number
        self.artists_ids = list()
        for artists in tracks.artists :
            self.artists_ids.append(artists.id)
        self.album_id = tracks.album.id

class SearchTracks(BaseModel) :
    href: str
    limit: int
    next: Union[str, None]
    offset: int
    previous: Union[str, None]
    total: int
    items: List[Tracks]

class SearchAlbums(BaseModel) :
    href: str
    limit: int
    next: Union[str, None]
    offset: int
    previous: Union[str, None]
    total: int
    items: List[Albums]

class SearchArtists(BaseModel) :
    href: str
    limit: int
    next: Union[str, None]
    offset: int
    previous: Union[str, None]
    total: int
    items: List[Artists]

class Search(BaseModel) :
    # artists: SearchArtists
    # albums: SearchAlbums
    tracks: SearchTracks