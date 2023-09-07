from model.database import Base
from pydantic import BaseModel, ConfigDict

from sqlalchemy.sql.schema import Column
from sqlalchemy import String
a = 0 
class SpotifyClientORM(Base) :
    __tablename__ = 'spotify_client'

    user = Column(String, nullable=True)
    id = Column(String, primary_key=True)
    secret = Column(String, nullable=False)
    redirect_uri = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)

    def __init__(self, client) :
        self.user = client.get('user')
        self.id = client.get('id')
        self.secret = client.get('secret')
        self.redirect_uri = client.get('redirect_uri')
        self.refresh_token = 'BQAJxyjBU6xzXJZsdXlF2E79Q-m7bUKub7zHQdUOR5ziWp4MWcuvnzdBFrdQgfqo6igRaFMuJ60oD6PUgcUNfJBalRwiLFMtMP0FJW8r1lGBcBonNRx28MLU6SjCOleWOIU8VI3xFQ4kf4AAtQjII8UGONJuM7v_MQ3F0MJokjYizVNWbv7OTUBkpVmxrSDYz6b00c9LYQ'

class SpotifyClientEntity(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    user: str
    id: str
    secret: str
    redirect_uri: str
    refresh_token: str

if __name__ == '__main__' :
    from sqlalchemy import inspect
    mapper = inspect(SpotifyClientORM)
    table_name = mapper.persist_selectable.name
    column_names = [column.key for column in mapper.columns]

    print("Column Names:", column_names)
    print("Table Name:", table_name)
    print("Column Names:", column_names)
