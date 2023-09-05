from model.spotify_artists import SpotifyArtistsORM, SpotifyArtistsEntity
from model.spotify_albums import SpotifyAlbumsORM, SpotifyAlbumsEntity
from model.spotify_tracks import SpotifyTracksORM, SpotifyTracksEntity

from get_token import return_token

import requests, json

if __name__ == '__main__':
    access_token = return_token()

    response = requests.get('https://api.spotify.com/v1/search?'
                            +'q=아이유'
                            +'&type=artist%2Calbum%2Ctrack'
                      ,headers={
                          'Authorization': 'Bearer '+ access_token
                      }
                      )
    if response.status_code == 200 :
        result = response.json()

        artists = result.get('artists').get('items')
        albums = result.get('albums').get('items')
        tracks = result.get('tracks').get('items')

    for artist in artists :
        artist_orm = SpotifyArtistsORM(artist)
        print(artist_orm.name)
        
    
    for album in albums :
        album_orm = SpotifyAlbumsORM(album)
        print(album_orm.name)

    for track in tracks :
        track_orm = SpotifyTracksORM(track)
        print(track_orm.name)