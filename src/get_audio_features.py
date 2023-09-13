import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.database import session_scope
import model.audio_features as Audio

import requests

if __name__ == '__main__' :

    from src.get_token import update_token, return_token
    access_token = return_token()
    # access_token = update_token('iamsophie')

    response = requests.get('https://api.spotify.com/v1/audio-features/'
                 +'02SbQgZbzMoylPoGr32ugF'
            ,headers={
                'Authorization': 'Bearer '+ access_token
            }
            )
    if response.status_code == 200 :
        responsed_data = response.json()
        
        parsed_data = Audio.SpotifyAudioFeatures(**responsed_data)
        orm = Audio.SpotifyAudioFeaturesORM(parsed_data)
        
        with session_scope() as session :
            session.add(orm)

    else : print(response.status_code)