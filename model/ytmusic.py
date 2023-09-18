#youtube model
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union

class DefaultInfo(BaseModel):
    url:str
class ThumbnailInfo(BaseModel):
    default:DefaultInfo
class Snippet(BaseModel):
    title: str
    thumbnails: ThumbnailInfo
    position: int

class ContentDetails(BaseModel):
    videoPublishedAt: str
class js_ChartYoutube(BaseModel) :
    snippet: Snippet
    contentDetails: ContentDetails

class js_SumChart(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    result_item: List[js_ChartYoutube]
    
class hy_ChartYoutube(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    title: str
    artist: str
    rank_const: str
    change: str 
    view: str 
    previous_rank: Union[str,None] 
    url: str 
    video_Id: str
    
class Response(BaseModel) :
    model_config = ConfigDict(from_attributes=True)
    args: List[hy_ChartYoutube]


    