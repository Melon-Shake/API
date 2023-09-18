from model.database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean

class SpotifyTokenORM(Base) :
    __tablename__ = 'spotify_token'

    id = Column(Integer, primary_key=True)
    value = Column(String, nullable=False)
    is_expired = Column(Boolean, default=False)
    
    def __init__(self,token):
        self.value = token

class SpotifyTokenEntity(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    id: int
    value: str
    is_expired: bool

if __name__ == '__main__' :
    from sqlalchemy import inspect
    mapper = inspect(SpotifyTokenORM)
    table_name = mapper.persist_selectable.name
    column_names = [column.key for column in mapper.columns]