from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union

from model.spotify_artists import SpotifyArtists

class SpotifySearchArtists(BaseModel) :
    href: str
    limit: int
    next: Union[str, None]
    offset: int
    previous: Union[str, None]
    total: int
    items: List[SpotifyArtists]

class SpotifySearch(BaseModel) :
    artists: SpotifySearchArtists