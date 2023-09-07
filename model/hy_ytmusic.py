from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union

class ChartYoutube(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    artist: str
    
class Response(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    
    args: List[ChartYoutube]