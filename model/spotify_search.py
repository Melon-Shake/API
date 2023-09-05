from pydantic import BaseModel
from typing import Dict, List, Union

class SpotifyArtists(BaseModel) :
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
    access_token = 'BQDISv37-0sT-nwXNif8X6fvP4NRNL06Qu7WhtgFsi1EVrFUyGSkm25cm9Zoz1Gnpz-pu5dbQDjp8uMsI04mEUMnIhcsVWj1j7E4NXkBCl5o32MrpQ3mRAm6UrLiOLhYbVgu1-zCvd-hvO1gs_IaOQepIy1feH7Cd7eKr0E-5e6qYMezrLTk2EGjVqf2OPTqegijFzzALQ'
    response = requests.get('https://api.spotify.com/v1/search?'
                            +'q=아이유'
                            +'&type=artist%2Calbum%2Ctrack'
                      ,headers={
                          'Authorization': 'Bearer '+ access_token
                      }
                      )
    if response.status_code == 200 :
        responsed_data = response.json()
        # print(responsed_data)
        parsed_data = SpotifySearch(**responsed_data)
        print(type(parsed_data))
        print(type(parsed_data.artists))
        print(type(parsed_data.artists.items))
        x = parsed_data.artists.items[0].uri
        print(type(x))
        print(x)

    else : print(response.status_code)
    
    