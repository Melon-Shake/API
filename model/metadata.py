from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union, Optional

class Artist(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    name: str
    img: Optional[str]
    
class Album(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    name: str
    img: Optional[str]
    artists: str
    release_year: str
<<<<<<< HEAD

# class AlbumExt(Album) :
#     model_config = ConfigDict(from_attributes=True)
=======
>>>>>>> v0.3.0/dev
    
class Track(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    name: str
    img: Optional[str]
    duration: str
    artists: str
    
class SearchResult(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    artists: List[Artist]
    albums: List[Album]
    tracks: List[Track]
