from model.database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column

class SpotifyTracksORM(Base) :
    pass

class SpotifyTracksEntity(BaseModel) :
    pass