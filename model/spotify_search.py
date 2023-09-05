from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union
from database import Base
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
        self.id = artists.get('id')
        self.name = artists.get('name')
        self.uri = artists.get('uri')
        self.href = artists.get('href')
        self.external_urls = artists.get('external_urls').get('spotify')
        self.images_url = artists.get('images')[0].get('url')
        self.popularity = artists.get('popularity')
        self.followers_total = artists.get('followers').get('total')
        self.genres = artists.get('genres')

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

if __name__ == '__main__':
    import requests
    access_token = 'BQAVXHCFzLIt4y1K4E9EGK7Ml337hn2gbq5Kd84b_dXzACtvXUJnZL1nejwlC-mWupkzPah4_EyRXjUbbkht-DZsiW11od-Z1HQ0JAdWT30YxoSPhJKrbNIYXR27SiJ4ZhL4l3rmIJuar4LAza_B2rSO9BF_ibe0XwoMJtrqjXafYBbhSUI_0_A3XXPEJUswMWyNTRXYDQ'
    response = requests.get('https://api.spotify.com/v1/search?'
                            +'q=아이유'
                            +'&type=artist%2Calbum%2Ctrack'
                      ,headers={
                          'Authorization': 'Bearer '+ access_token
                      }
                      )
    if response.status_code == 200 :
        responsed_data = response.json()
        parsed_data = SpotifySearch(**responsed_data)
        artists = parsed_data.artists.items

        for entity in artists :
            orm = SpotifyArtistsORM(entity.__dict__)

            from database import session_scope
            with session_scope() as session :
                session.add(orm)

    else : print(response.status_code)
    
    