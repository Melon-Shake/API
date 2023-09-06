from model.database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean

class SpotifyArtistsORM(Base) :
    __tablename__ = 'sp_artists'

    external_urls = Column(String, nullable=True)
    genres = Column(String, nullable=True)
    href = Column(String, nullable = True)
    id = Column(String,primary_key=True)
    images_url =Column(String,nullable = True)
    name = Column(String,nullable = True)
    popularity = Column(Integer,nullable=True)
    type = Column(String,nullable = True)
    uri = Column(String,nullable = True)
    
    def __init__(self, external_urls, genres, href, id, images_url, name, popularity, type, uri):
        self.external_urls = external_urls
        self.genres = genres
        self.href = href
        self.id = id
        self.images_url = images_url
        self.name = name
        self.popularity = popularity
        self.type = type
        self.uri = uri
class SpotifyArtistsEntity(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    extertnal_urls: str
    genres: str
    href: str
    id :str
    images_url : str
    name : str
    popularity : int
    type :str
    uri : str


if __name__ == '__main__' :
    from sqlalchemy import inspect
    mapper = inspect(SpotifyTokenORM)
    table_name = mapper.persist_selectable.name
    print("Table Name:", table_name)
    column_names = [column.key for column in mapper.columns]
    print("Column Names:", column_names)