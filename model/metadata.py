from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union, Optional

class Artist(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    img: Optional[str]
    
class Album(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    img: Optional[str]
    artist: str
    release_year: str
    
class Track(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    id: str
    album_id: str
    name: str
    img: Optional[str]
    duration: str
    artist: str
    
class SearchResult(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    artists: List[Artist]
    albums: List[Album]
    tracks: List[Track]
