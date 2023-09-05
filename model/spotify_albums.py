from model.database import Base
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
    # artists_id = Column(String, nullable=True)
    # tracks_ids = Column(String, nullable=True)

    def __init__(self, albums) :
        self.id = albums.get('id',None)
        self.name = albums.get('name',None)
        self.uri = albums.get('uri',None)
        self.href = albums.get('href',None)
        self.external_urls = albums.get('external_urls',None)
        self.images_url = albums.get('images_url',None)
        self.genres = albums.get('genres',None)
        self.popularity = albums.get('popularity',None)
        self.album_type = albums.get('album_type',None)
        self.total_tracks = albums.get('total_tracks',None)
        self.available_markets = albums.get('available_markets',None)
        self.release_date = albums.get('release_date',None)
        self.release_date_precision = albums.get('release_date_precision',None)
        
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