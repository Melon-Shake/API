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
    culled_data = Search.cull_data(parsed_data)
    search_data = Search.return_search(culled_data)
    Search.load_spotify(culled_data)
    return search_data