from sqlalchemy import String
from sqlalchemy.sql.schema import Column

from config.database import Base

class SpotifyClient(Base) :
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