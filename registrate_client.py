from model.spotify_client import SpotifyClientORM, SpotifyClientEntity
from model.database import session_scope

import requests
import json

if __name__ == '__main__':
    
    client = {
        'user': 'iamsophie'
        , 'id': '42bf3e0e18094c5a8bdd940eb278ca5d'
        , 'secret': '696d03cb2ad84ac693342793df26bc09'
        , 'redirect_uri': 'http://localhost:8000/callback'
     }
    
    # with session_scope() as session :
    #     client_orm = SpotifyClientORM(client)
    #     session.add(client_orm)

    with session_scope() as session :
        client_orm = session.query(SpotifyClientORM).filter_by(user=client.get('user')).first()
        client_entity = SpotifyClientEntity.model_validate(client_orm)
        client_json = SpotifyClientEntity.model_dump_json(client_entity)

        response_post = requests.post('http://localhost:8000/registrate'
                                 ,headers={'Content-Type': 'application/json'}
                                 ,data=client_json
                                 )
        if response_post.status_code == 200 :
            result_post = response_post.json()
        else :
            print(response_post.status_code)
        
        response_get = requests.get('http://localhost:8000/registrate?'
                                    +f'id={client.get("id")}'
                                    +f'&redirect_uri={client.get("redirect_uri")}'
                                    )
        if response_get.status_code == 200 :
            result_get = response_get.json()
        else :
            print(response_get.status_code)