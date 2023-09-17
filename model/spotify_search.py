from model.database import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Integer, Float, ARRAY
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union, Optional

class Followers(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    total: Optional[int]

class Images(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    url: str

class ExternalUrls(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    spotify: str

class Artists(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    id: str
    uri: str
    href: str
    external_urls: ExternalUrls
    name: str

class ArtistsExt(Artists) :
    model_config = ConfigDict(from_attributes=True)
    images: List[Images]
    followers: Followers
    popularity: int
    genres: List[str]

class Albums(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    id: str
    uri: str
    href: str
    external_urls: ExternalUrls
    name: str
    images: List[Images]
    album_type: str
    total_tracks: int
    release_date: str
    release_date_precision: str
    artists: List[Artists]

class AlbumsExt(Albums) :
    model_config = ConfigDict(from_attributes=True)

class Tracks(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    id: str
    uri: str
    href: str
    external_urls: ExternalUrls
    name: str
    duration_ms: int
    track_number: int
    disc_number: int
    album: Albums
    artists: List[Artists]

class TracksExt(Tracks) :
    model_config = ConfigDict(from_attributes=True)
    popularity: int

class SearchArtists(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    href: str
    limit: int
    next: Optional[str]
    offset: int
    previous: Optional[str]
    total: int
    items: List[ArtistsExt]

class SearchAlbums(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    href: str
    limit: int
    next: Optional[str]
    offset: int
    previous: Optional[str]
    total: int
    items: List[AlbumsExt]

class SearchTracks(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    href: str
    limit: int
    next: Optional[str]
    offset: int
    previous: Optional[str]
    total: int
    items: List[TracksExt]

class Search(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    artists: Optional[SearchArtists]
    albums: Optional[SearchAlbums]
    tracks: Optional[SearchTracks]

class SearchResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    artists: List[ArtistsExt]
    tracks: List[TracksExt]
    albums: List[AlbumsExt]

class SearchKeyword(BaseModel):
    searchInput : str

class ArtistsORM(Base) :
    __tablename__ = 'spotify_artists'

    id = Column(String, primary_key=True)
    uri = Column(String, nullable=True)
    href = Column(String, nullable=True)
    external_urls = Column(String, nullable=True)
    name = Column(String, nullable=True)
    images_url = Column(String, nullable=True)
    followers_total = Column(Integer, nullable=True)
    popularity = Column(Integer, nullable=True)
    genres = Column(String, nullable=True)

    def __init__(self,artists:Artists):
        self.id = artists.id
        self.uri = artists.uri
        self.href = artists.href
        self.external_urls = artists.external_urls.spotify
        self.name = artists.name
        images = getattr(artists,'images',None)
        self.images_url = images[0].url if images and images[0].url else None
        followers = getattr(artists,'followers',None)
        self.followers_total = getattr(followers,'total',None)
        self.popularity = getattr(artists,'popularity',None)
        self.genres = getattr(artists,'genres',None)

class AlbumsORM(Base) :
    __tablename__ = 'spotify_albums'

    id = Column(String, primary_key=True)
    uri = Column(String, nullable=True)
    href = Column(String, nullable=True)
    external_urls = Column(String, nullable=True)
    name = Column(String, nullable=True)
    images_url = Column(String, nullable=True)
    album_type = Column(String, nullable=True)
    total_tracks = Column(Integer, nullable=True)
    release_date = Column(String, nullable=True)
    release_date_precision = Column(String, nullable=True)

    def __init__(self, albums:Albums) :
        self.id = albums.id
        self.uri = albums.uri
        self.href = albums.href
        self.external_urls = albums.external_urls.spotify
        self.name = albums.name
        self.images_url = albums.images[0].url
        self.album_type = albums.album_type
        self.total_tracks = albums.total_tracks
        self.release_date = albums.release_date
        self.release_date_precision = albums.release_date_precision

class TracksORM(Base) :
    __tablename__ = 'spotify_tracks'

    id = Column(String, primary_key=True)
    uri = Column(String, nullable=True)
    href = Column(String, nullable=True)
    external_urls = Column(String, nullable=True)
    name = Column(String, nullable=True)
    popularity = Column(Integer, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    track_number = Column(Integer, nullable=True)
    disc_number = Column(Integer, nullable=True)
    album_id = Column(String, nullable=True)
    artists_ids = Column(ARRAY(String), nullable=True)

    def __init__(self, tracks:Tracks) :
        self.id = tracks.id
        self.uri = tracks.uri
        self.href = tracks.href
        self.external_urls = tracks.external_urls.spotify
        self.name = tracks.name
        self.duration_ms = tracks.duration_ms
        self.track_number = tracks.track_number
        self.disc_number = tracks.disc_number
        self.album_id = tracks.album.id
        self.artists_ids = list()
        for artists in tracks.artists :
            self.artists_ids.append(artists.id)
        self.popularity = getattr(tracks,'popularity',None)

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