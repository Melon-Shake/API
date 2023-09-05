from database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column
from sqlalchemy import String

class SpotifyAlbumsORM(Base) :
    __tablename__ = 'spotify_albums'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    uri = Column(String, nullable=True)
    href = Column(String, nullable=True)
    external_urls = Column(String, nullable=True)
    images_url = Column(String, nullable=True)
    genres = Column(String, nullable=True)
    popularity = Column(String, nullable=True)
    album_type = Column(String, nullable=True)
    total_tracks = Column(String, nullable=True)
    available_markets = Column(String, nullable=True)
    release_date = Column(String, nullable=True)
    release_date_precision = Column(String, nullable=True)
    artists_id = Column(String, nullable=True)
    tracks_ids = Column(String, nullable=True)

class SpotifyAlbumsEntity(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    images_url: str
    release_date_precision: str
    artists_id: str
    artists_name: str

if __name__ == '__main__' :
    from sqlalchemy import inspect
    mapper = inspect(SpotifyAlbumsORM)
    table_name = mapper.persist_selectable.name
    column_names = [column.key for column in mapper.columns]
    print("Table Name:", table_name)
    print("Column Names:", column_names)