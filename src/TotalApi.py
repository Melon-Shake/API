from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
import pandas as pd
import lib.module as module
from pydantic import BaseModel
import bcrypt
import psycopg2
from datetime import datetime
from config.db_info import db_params
from lyric import lyric_search_and_input
from get_token import return_token
from typing import Dict, List, Union
from model.database import session_scope
from model.jun_model import *
from get_keyword import save_keyword_data
from user_data import user_data
from user_search_track import pick_data
from daily_search_ranking import daily_search_ranking
from make_playlist import make_playlist
from search_spotify import *
from model.spotify_search import *


app = FastAPI()

@app.get('/token/')
def update_token():
    access_token = return_token()
    return access_token

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

    parsed_data = Search.search_by_keywords(data.searchInput,limit=10)
    culled_data = Search.cull_data(parsed_data.tracks)
    Search.load_spotify(culled_data)

    album_ids = [album.id for album in culled_data.albums]
    for album_id in album_ids :
        Search.get_album_tracks(album_id)
    
    # artist_ids = [artist.id for artist in culled_data.artists]
    # for artist_id in artist_ids :
    #     Search.get_artist_albums(artist_id)

@app.post("/get_user_data/")
def get_user_data(data: LoginData):
   user_data(data, db_params)
    
@app.post("/get_keyword_data/")
def get_keyword_data(data: Keyword): 
    save_keyword_data(data, db_params)

@app.post("/get_use_data/")
def get_use_data(data: search_track):
    pick_data(data,db_params)
    
@app.post("/daily_search_ranking/")
def get_daily_search_ranking():
    search_ranking_result = daily_search_ranking()
    return search_ranking_result

@app.post('/playlist/')
def get_playlist(data:playlist):
    return make_playlist(data,5,db_params)