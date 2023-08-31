from model.spotify_token import SpotifyTokenORM, SpotifyTokenEntity
from model.database import session_scope

if __name__ == '__main__' :
    orm = SpotifyTokenORM({'id':1,'value':'aaaa','is_expired':False})
    entity = SpotifyTokenEntity.model_validate(orm)
    
    print(type(orm))
    print(orm)
    print(type(entity))
    print(entity)