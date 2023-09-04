from model.database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column

class SpotifyAlbumsORM(Base) :
    pass

class SpotifyAlbumsEntity(BaseModel) :
    pass