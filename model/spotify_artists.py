from model.database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column
from sqlalchemy import String

class SpotifyArtistsORM(Base) :
    __tablename__ = 'spotify_artists'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    uri = Column(String, nullable=True)
    href = Column(String, nullable=True)
    external_urls = Column(String, nullable=True)
    images_url = Column(String, nullable=True)
    genres = Column(String, nullable=True)
    popularity = Column(String, nullable=True)

    def __init__(self, artists) :
        self.id = artists.get('id', None)
        self.name = artists.get('name', None)
        self.uri = artists.get('uri', None)
        self.href = artists.get('href', None)
        self.external_urls = artists.get('external_urls', None)
        self.images_url = artists.get('images_url', None)
        self.genres = artists.get('genres', None)
        self.popularity = artists.get('popularity', None)

class SpotifyArtistsEntity(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    images_url: str

if __name__ == '__main__' :
    from sqlalchemy import inspect
    mapper = inspect(SpotifyArtistsORM)
    table_name = mapper.persist_selectable.name
    column_names = [column.key for column in mapper.columns]
    print("Table Name:", table_name)
    print("Column Names:", column_names)