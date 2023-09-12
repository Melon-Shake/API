
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

def update_token(user) :
    with session_scope() as session :
        client = session.query(SpotifyClientORM).filter_by(user=user).one()

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
    
if __name__ == '__main__' :
    user = 'iamsophie'
    token_updated = update_token(user)
    token_latest = return_token()
    try:
        assert token_updated == token_latest
    except AssertionError as e :
        print("새로 갱신된 액세스 토큰 :" + token_updated)
        print("가장 최근 액세스 토큰 :" + token_latest)