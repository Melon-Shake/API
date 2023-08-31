from sqlalchemy import String
from sqlalchemy.sql.schema import Column

from config.database import Base
from pydantic import BaseModel, ConfigDict

class SpotifyClientORM(Base) :
    __tablename__ = 'spotify_client'

    user = Column(String, nullable=True)
    id = Column(String, primary_key=True)
    secret = Column(String, nullable=False)
    redirect_uri = Column(String, nullable=False)

    def __init__(self, client) :
        self.user = client.get('user')
        self.id = client.get('id')
        self.secret = client.get('secret')
        self.redirect_uri = client.get('redirect_uri')

class SpotifyClientEntity(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    user: str
    id: str
    secret: str
    redirect_uri: str