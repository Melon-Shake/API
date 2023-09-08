from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union
from typing import List, Optional

class Artistinfo(BaseModel):
  ARTISTID: str
  ARTISTNAME: str
# 
class GenreInfo(BaseModel):
  GENRECODE: Union[str, int]
  GENRENAME: Union[str, int]
  

class ChartMelon(BaseModel):
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
