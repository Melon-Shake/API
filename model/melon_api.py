from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union
from typing import List, Optional

# from model.

class ChartMelon(BaseModel):
  SONGID: int
  SONGNAME: str
  ALBUMID: int
  ALBUMNAME: str
  ARTISTID: List[Dict[str,Union[str,int]]]
  ARTISTNAME: List[Dict[str,Union[str,None]]]
  GENRECODE: List[Dict[str, Union[str, None]]]
  # GENRENAME: List[Dict[str, Union[str, None]]]