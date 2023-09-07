from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union

# from model.

class ChartMelon(BaseModel):
  SONGID: int
  # SONGNAME: str
  # ALBUMID: str
  # ALBUMNAME: str
  # ARTISTID: List[Dict[str,Union(str,None)]]
  # ARTISTNAME: List[Dict[str,Union(str,None)]]