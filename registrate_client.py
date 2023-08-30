from model.spotify_client import SpotifyClient
from config.database import session_scope, engine

def set(client):
    with session_scope() as session :
        session.add(client)
        session.commit()

def get(client_user):
    with session_scope() as session :
        clients = session.query(SpotifyClient).all()
        for client in clients :
            if client.user == client_user :
                return SpotifyClient(client.user,client.id,client.secret,client.redirect_uri)

if __name__ == '__main__':

    client_set = SpotifyClient(user='iamsophie'
        ,id='42bf3e0e18094c5a8bdd940eb278ca5d'
        ,secret='696d03cb2ad84ac693342793df26bc09'
        ,redirect_uri='http://localhost:3000/callback'
    )
    set(client_set)
    client = get('iamsophie')