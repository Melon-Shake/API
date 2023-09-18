import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

import model.spotify_search as Spotify
import src.search_spotify as Search
from src.get_token import update_token, return_token

app = FastAPI()

@app.post('/search/')
async def search_spotify(data:Spotify.SearchKeyword):
    access_token = update_token()
    search_header = {'Authorization': f'Bearer {access_token}'}

    parsed_data = Search.search_by_keywords(data.searchInput,limit=10)
    culled_data = Search.cull_data(parsed_data.tracks)
    
    search_data = Search.return_search(culled_data)
    return search_data

@app.post('/load/')
async def load_spotify(data:Spotify.SearchKeyword):
    access_token = update_token()
    search_header = {'Authorization': f'Bearer {access_token}'}

    parsed_data = Search.search_by_keywords(data.searchInput,limit=1)
    culled_data = Search.cull_data(parsed_data.tracks)
    Search.load_spotify(culled_data)

    album_ids = [album.id for album in culled_data.albums]
    for album_id in album_ids :
        Search.get_album_tracks(album_id)
    
    # artist_ids = [artist.id for artist in culled_data.artists]
    # for artist_id in artist_ids :
    #     Search.get_artist_albums(artist_id)
