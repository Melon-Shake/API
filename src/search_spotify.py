import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.database import session_scope
from model.spotify_artists import SpotifyArtists, SpotifyArtistsORM
from model.spotify_albums import SpotifyAlbums, SpotifyAlbumsORM
from model.spotify_search import SpotifySearch, SpotifySearchArtists

from src.get_token import update_token, return_token

import requests

if __name__ == '__main__':
    # update_token('iamsophie')
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
        # print(responsed_data.get('albums').get('items')[0])

        parsed_data = SpotifySearch(**responsed_data)

        artists = parsed_data.artists.items
        for entity in artists :
            orm = SpotifyArtistsORM(entity)
            with session_scope() as session :
                session.add(orm)

        albums = parsed_data.albums.items
        for entity in albums :
            orm = SpotifyAlbumsORM(entity)
            with session_scope() as session :
                session.add(orm)