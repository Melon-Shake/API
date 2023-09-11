import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.database import session_scope
import model.spotify_search as Spotify

from src.get_token import update_token, return_token

import requests

def search_spotify(input:str) :
    access_token = return_token()
    response = requests.get('https://api.spotify.com/v1/search?'
                            +'q={keyword}'.format(keyword=input)
                            +'&type=artist%2Calbum%2Ctrack'
                      ,headers={
                          'Authorization': 'Bearer '+ access_token
                      }
                      )
    
    if response.status_code == 200 :
        responsed_data = response.json()
        parsed_data = Spotify.Search(**responsed_data)
        return parsed_data

def load_spotify(data:Spotify.Search) :
    with session_scope() as session :
        for entity in data.tracks.items :
            tracks = Spotify.TracksORM(entity)
            albums = Spotify.AlbumsORM(entity.album)
            artists = [Spotify.ArtistsORM(e) for e in entity.artists]
            session.add(tracks)
            session.add(albums)
            session.add_all(artists)

if __name__ == '__main__':
    # update_token('iamsophie')
    access_token = return_token()

    search_result = search_spotify('아이유')
    load_spotify(search_result)