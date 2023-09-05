from database import Base
from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.schema import Column
from sqlalchemy import String

class SpotifyTracksORM(Base) :
    __tablename__ = 'sp_tracks'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    uri = Column(String, nullable=True)
    href = Column(String, nullable=True)
    external_urls = Column(String, nullable=True)
    duration_ms = Column(String, nullable=True)
    explicit = Column(String, nullable=True)
    restrictions_reason = Column(String, nullable=True)
    is_playable = Column(String, nullable=True)
    linked_form = Column(String, nullable=True)
    available_markets = Column(String, nullable=True)
    disc_number = Column(String, nullable=True)
    track_number = Column(String, nullable=True)
    popularity = Column(String, nullable=True)
    preview_url = Column(String, nullable=True)
    is_local = Column(String, nullable=True)
    albums_id = Column(String, nullable=True)
    artists_ids = Column(String, nullable=True)

class SpotifyTracksEntity(BaseModel) :
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    albums_id: str
    albums_images_url: str
    artists_ids: str
    artists_names: str
    duration_ms: str

if __name__ == '__main__' :
    from sqlalchemy import inspect
    mapper = inspect(SpotifyTracksORM)
    table_name = mapper.persist_selectable.name
    column_names = [column.key for column in mapper.columns]
    print("Table Name:", table_name)
    print("Column Names:", column_names)