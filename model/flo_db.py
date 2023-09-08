from model.database import Base, engine
from sqlalchemy.sql.schema import Column
from sqlalchemy import Integer, String, Boolean, JSON, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship

from model.chart_flo import ChartFlo

class FloTrack(Base) :
    __tablename__ = 'flo_tracks'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)

    chart = relationship('FloChart', back_populates='track')

class FloAlbum(Base) :
    __tablename__ = 'flo_albums'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    release_ymd = Column(String, nullable=True)
    img_url = Column(String, nullable=True)

    chart = relationship('FloChart', back_populates='album')

    def __init__(self, album) :
        self.id = album.id
        self.title = album.title
        self.release_ymd = album.releaseYmd
        self.img_url = album.imgList[0].url

class FloArtist(Base) :
    __tablename__ = 'flo_artists'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)

    chart = relationship('FloChart', back_populates='artist')

    def __init__(self, artist) :
        self.id = artist.id
        self.name = artist.name

class FloChart(Base) :
    __tablename__ = 'flo_chart'

    id = Column(Integer, primary_key=True)
    
    rank = Column(Integer)
    points = Column(Integer)
    created_datetime = Column(DateTime)

    artist_id = Column(Integer, ForeignKey('flo_artists.id'))
    album_id = Column(Integer, ForeignKey('flo_albums.id'))
    track_id = Column(Integer, ForeignKey('flo_tracks.id'))

    artist = relationship('FloArtist', back_populates='chart')
    album = relationship('FloAlbum', back_populates='chart')
    track = relationship('FloTrack', back_populates='chart')

    def __init__(self, index, artist, album, track):
        self.rank = index+1
        self.points = self.rank*6.1
        self.artist = artist
        self.album = album
        self.track = track