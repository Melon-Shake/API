from fastapi import FastAPI
import uvicorn

from model.spotify_client import SpotifyClientEntity


api = FastAPI()

@api.get('/')
def index():
    return '안녕'

@api.post('/registrate')
def registrate(client:SpotifyClientEntity):
    return client

@api.get('/registrate')
def registrate(id:str,redirect_uri:str) :
    return id+redirect_uri

from update_token import return_token
@api.get('/token')
def update_token():
    access_token = return_token()
    return access_token

if __name__ == "__main__":
    uvicorn.run(api, host="127.0.0.1", port=8000)