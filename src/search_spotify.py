import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.database import session_scope
import model.spotify_search as Spotify

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

        parsed_data = Spotify.Search(**responsed_data)
        artists = parsed_data.artists.items
        albums = parsed_data.albums.items
        tracks = parsed_data.tracks.items

        for entity in artists :
            orm = Spotify.ArtistsORM(entity)
            with session_scope() as session :
                session.add(orm)

        for entity in albums :
            orm = Spotify.AlbumsORM(entity)
            with session_scope() as session :
                session.add(orm)

        for entity in tracks :
            orm = Spotify.TracksORM(entity)
            with session_scope() as session :
                session.add(orm)