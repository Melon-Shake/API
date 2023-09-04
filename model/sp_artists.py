from model.database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column

class SpotifyArtistsORM(Base) :
    pass

class SpotifyArtistsEntity(BaseModel) :
    pass