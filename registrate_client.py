from model.spotify_client import SpotifyClientORM, SpotifyClientEntity
# from config.database import session_scope

import requests
import json

# def set(client):
#     with session_scope() as session :
#         session.add(client)
#         session.commit()

# def get(client_user):
#     with session_scope() as session :
#         clients = session.query(SpotifyClientORM).all()
#         for client in clients :
#             if client.user == client_user :
#                 return SpotifyClientORM(client.user,client.id,client.secret,client.redirect_uri)

if __name__ == '__main__':

    client = SpotifyClientORM(user='iamsophie'
        ,id='42bf3e0e18094c5a8bdd940eb278ca5d'
        ,secret='696d03cb2ad84ac693342793df26bc09'
        ,redirect_uri='http://localhost:8000/callback'
    )
    # client.set(client)
    client_orm = client.get('iamsophie')

    print(type(client_orm))
    print(client_orm)

    client_entity = SpotifyClientEntity.model_validate(client_orm)

    print(type(client_entity))
    print(client_entity)

    data = json.dumps(client_entity.__dict__)
    print(type(data))
    print(data)
    header = {"Content-Type": "application/json"}

    response = requests.post('http://localhost:8000/test',data=data, headers=header)
    print(response.status_code)

    if response.status_code == 200 :
        result = response.json()
        print(result)