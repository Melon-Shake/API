from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
import requests
import base64
import config.client as client

from model.spotify_client import SpotifyClientEntity

client_id = client.ID
client_secrets = client.SECRETS
redirect_uri = client.REDIRECT_URI

api = FastAPI()

def func_base64(input):
    input_byte = input.encode()
    output_byte = base64.b64encode(input_byte)
    output = output_byte.decode()
    return output

@api.post('/test')
def test(client: SpotifyClientEntity):
    response = requests.get('https://accounts.spotify.com/authorize?'
                            +f'client_id={client.id}'
                            +f'&redirect_uri={client.redirect_uri}'
                            +f'&response_type=code'
                            )
    return response.text

@api.get("/authorize")
def authorize():
    return RedirectResponse(
        url=f'https://accounts.spotify.com/authorize?'
        +f'client_id={client.id}'
        +f'&redirect_uri={client.redirect_uri}'
        +f'&response_type=code'
    )

@api.get("/callback")
def callback(code: str):
    response = requests.post('https://accounts.spotify.com/api/token',
                             data={
                                 'grant_type': 'authorization_code',
                                 'code': code,
                                 'redirect_uri': redirect_uri
                             },
                             headers={
                                 'Authorization': 'Basic ' + func_base64(client_id + ':' + client_secrets)
                             }
                             )

    if response.status_code == 200:
        response_json = response.json()
        refresh_token = response_json.get('refresh_token', None)
        access_token = response_json.get('access_token', None)
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to get access token")

@api.get("/refresh_token")
def refresh_token(refresh_token: str):
    response = requests.post('https://accounts.spotify.com/api/token',
                             data={
                                 'grant_type': 'refresh_token',
                                 'refresh_token': refresh_token
                             },
                             headers={
                                 'Authorization': 'Basic ' + func_base64(client_id + ':' + client_secrets)
                             }
                             )

    if response.status_code == 200:
        response_json = response.json()
        access_token = response_json.get('access_token', None)
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to refresh token")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host="127.0.0.1", port=8000)