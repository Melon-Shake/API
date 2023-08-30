from sqlalchemy import String
from sqlalchemy.sql.schema import Column

from config.database import Base, session_scope
from pydantic import BaseModel, ConfigDict

class SpotifyClientORM(Base) :
    __tablename__ = 'spotify_client'

    user = Column(String, nullable=True)
    id = Column(String, primary_key=True)
    secret = Column(String, nullable=False)
    redirect_uri = Column(String, nullable=False)

    def __init__(self, user=None, id=None, secret=None, redirect_uri=None):
        self.user = user
        self.id = id
        self.secret = secret
        self.redirect_uri = redirect_uri

    def set(self, client):
        with session_scope() as session :
            session.add(client)
            session.commit()

    def get(self, client_user):
        with session_scope() as session :
            clients = session.query(SpotifyClientORM).all()
            for client in clients :
                if client.user == client_user :
                    return SpotifyClientORM(client.user,client.id,client.secret,client.redirect_uri)

class SpotifyClientEntity(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    user: str
    id: str
    secret: str
    redirect_uri: str