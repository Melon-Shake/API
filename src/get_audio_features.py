import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.database import session_scope
import model.audio_features as Audio

import requests

def get_audio_features(id:str) :
    from get_token import return_token
    access_token = return_token()
    
    response = requests.get('https://api.spotify.com/v1/audio-features/'
                            +f'{id}'
                        ,headers={
                            'Authorization': 'Bearer '+ access_token
                        }
                        )
    if response.status_code == 200 :
        responsed_data = response.json()
        parsed_data = Audio.SpotifyAudioFeatures(**responsed_data)
        return parsed_data

def load_audio_features(id:str):
    parsed_data = get_audio_features(id)
    orm = Audio.SpotifyAudioFeaturesORM(parsed_data)
    with session_scope() as session :
        session.add(orm)

if __name__ == '__main__' :

    # 0 - get spotify token
    from src.get_token import update_token, return_token
    access_token = return_token()
    # access_token = update_token('iamsophie')

    # 1 - load db : spotify_audio_features
    spotify_track_id = '02SbQgZbzMoylPoGr32ugF'
    load_audio_features(spotify_track_id)

    # 1 확인
    with session_scope() as session :
        result = session.query(Audio.SpotifyAudioFeaturesORM).filter_by(id='02SbQgZbzMoylPoGr32ugF').one()
        print(type(result))
        print(result.acousticness)