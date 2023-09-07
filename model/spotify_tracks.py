from model.database import Base
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
    # albums_id = Column(String, nullable=True)
    # artists_ids = Column(String, nullable=True)

    def __init__(self, tracks) :
        self.id = tracks.get('id', None)
        self.name = tracks.get('name', None)
        self.uri = tracks.get('uri', None)
        self.href = tracks.get('href', None)
        self.external_urls = tracks.get('external_urls', None)
        self.duration_ms = tracks.get('duration_ms', None)
        self.explicit = tracks.get('explicit', None)
        self.restrictions_reason = tracks.get('restrictions_reason', None)
        self.is_playable = tracks.get('is_playable', None)
        self.linked_form = tracks.get('linked_form', None)
        self.available_markets = tracks.get('available_markets', None)
        self.disc_number = tracks.get('disc_number', None)
        self.track_number = tracks.get('track_number', None)
        self.popularity = tracks.get('popularity', None)
        self.preview_url = tracks.get('preview_url', None)
        self.is_local = tracks.get('is_local', None)

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