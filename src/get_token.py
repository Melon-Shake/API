
from model.spotify_token import SpotifyTokenORM, SpotifyTokenEntity
from model.spotify_client import SpotifyClientORM, SpotifyClientEntity
from model.database import session_scope

import requests, json

def func_base64(input):
    import base64
    input_byte = input.encode()
    output_byte = base64.b64encode(input_byte)
    output = output_byte.decode()
    return output    

def update_token(user='iamsophie') :
    with session_scope() as session :
        client = session.query(SpotifyClientORM).filter_by(user=user).first()

        response = requests.post('https://accounts.spotify.com/api/token'
                      ,headers={
                          'Authorization': 'Basic '+func_base64(f'{client.id}:{client.secret}')
                      }
                      ,data={
                          'grant_type': 'refresh_token'
                          ,'refresh_token': client.refresh_token
                      }
                      )
    if response.status_code == 200 :
        result = response.json()
        access_token = result.get('access_token')
    with session_scope() as session :
        token_orm = SpotifyTokenORM(access_token)
        session.add(token_orm)
    return access_token

def return_token():
    with session_scope() as session :
        from sqlalchemy import desc
        token_orm = session.query(SpotifyTokenORM).order_by(desc(SpotifyTokenORM.id)).first()
        return token_orm.value