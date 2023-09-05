from model.spotify_artists import SpotifyArtistsORM, SpotifyArtistsEntity
from model.spotify_albums import SpotifyAlbumsORM, SpotifyAlbumsEntity
from model.spotify_tracks import SpotifyTracksORM, SpotifyTracksEntity

from get_token import return_token, update_token
from model.database import session_scope

import requests, json

if __name__ == '__main__':
    # update_token('iamsophie')
    access_token = return_token()

    response = requests.get('https://api.spotify.com/v1/search?'
                            +'q=아이유'
                            # +'&type=artist%2Calbum%2Ctrack'
                            +'&type=artist'
                      ,headers={
                          'Authorization': 'Bearer '+ access_token
                      }
                      )
    if response.status_code == 200 :
        result = response.json()

        # artists = result.get('artists').get('items')
        # artists_entity = SpotifyArtistsEntity.model_validate_json(artists)
        
    artists = result.get('artists').get('items')
    for artist in artists :
        artist_orm = SpotifyArtistsORM(artist) 
        print('{type}  {value}'.format(
            type = type(artist_orm.genres)
            ,value = artist_orm.genres
        ))
        # print(artist_orm.name)
        # print(artist_orm.uri)
        # print(artist_orm.href)
        # print(artist_orm.external_urls)
        # print(artist_orm.images_url)
        # print(artist_orm.genres)
        # print(artist_orm.popularity)

    # albums = result.get('albums').get('items')
    # for album in albums :
    #     album_orm = SpotifyAlbumsORM(album)
    #     print(album_orm.name)

    # tracks = result.get('tracks').get('items')
    # for track in tracks :
    #     track_orm = SpotifyTracksORM(track)
    #     print(track_orm.name)