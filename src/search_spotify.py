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

        # with session_scope() as session :
        #     for entity in parsed_data.tracks.items :
        #         tracks = Spotify.TracksORM(entity)
        #         albums = Spotify.AlbumsORM(entity.album)
        #         artists = [Spotify.ArtistsORM(e) for e in entity.artists]
        #         session.add(tracks)
        #         session.add(albums)
        #         session.add_all(artists)
        
        # with session_scope() as session :
        #     rows = session.query(Spotify.TracksORM.artists_ids).distinct().all()
        #     ids_list = [id for row in rows for id in row]
        #     ids_unique = list(set(id for ids in ids_list for id in ids))
            
        #     ids_artists = session.query(Spotify.ArtistsORM.id).distinct().all()
        #     print(all(id_artists.id in ids_unique for id_artists in ids_artists))

        with session_scope() as session :
            rows = session.query(Spotify.TracksORM.album_id).distinct().all()
            ids_unique = list(row.album_id for row in rows)
            ids_albums = session.query(Spotify.AlbumsORM.id).distinct().all()
            print(all(id_albums.id in ids_unique for id_albums in ids_albums))