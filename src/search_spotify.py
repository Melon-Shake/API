from model.database import session_scope
from model.spotify_artists import SpotifyArtists, SpotifyArtistsORM
from model.spotify_search import SpotifySearch, SpotifySearchArtists

from src.get_token import update_token, return_token

import requests

if __name__ == '__main__':
    update_token('iamsophie')
    access_token = return_token()
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

            with session_scope() as session :
                session.add(orm)