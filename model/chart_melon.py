from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union
from typing import List, Optional

from model.database import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Integer, ARRAY, Float, DateTime
from sqlalchemy.sql import func

class Artistinfo(BaseModel):
  ARTISTID: str
  ARTISTNAME: str

class GenreInfo(BaseModel):
  GENRECODE: Union[str, int]
  GENRENAME: Union[str, int]
  
class ChartMelon(BaseModel):
  model_config = ConfigDict(from_attributes=True)

  SONGID: int
  SONGNAME: str
  ALBUMID: int
  ALBUMNAME: str
  ARTISTLIST : List[Artistinfo]
  GENRELIST: List[GenreInfo]
  CURRANK: int
  PASTRANK: str
  ALBUMIMG: str
  ISSUEDATE: str

class MelonORM(Base):
  __tablename__ = 'chart_melon'

  id = Column(Integer, primary_key=True)
  track_name = Column(String, nullable=True)
  album_name = Column(String, nullable=True)
  img_url = Column(String, nullable=True)
  cur_rank = Column(Integer, nullable=True)
  past_rank = Column(Integer, nullable=True)
  issue_date = Column(String, nullable=True)
  artist_names = Column(ARRAY(String), nullable=True)
  genre_name = Column(String, nullable=True)
  points = Column(Float, nullable=True)
  created_datetime = Column(DateTime(timezone=True), server_default=func.now())

  def __init__(self, entity):
    self.track_name = entity.SONGNAME
    self.album_name = entity.ALBUMNAME
    self.img_url = entity.ALBUMIMG
    self.cur_rank = entity.CURRANK
    self.past_rank = entity.PASTRANK
    self.issue_date = entity.ISSUEDATE
    self.artist_names = list()
    self.genre_name = entity.GENRELIST[0].GENRENAME
    self.points = (101-self.cur_rank)*32.8