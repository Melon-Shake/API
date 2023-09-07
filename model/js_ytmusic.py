from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Union
class DefaultInfo(BaseModel):
    url:str
class ThumbnailInfo(BaseModel):
    default:DefaultInfo
class Snippet(BaseModel):
    title: str
    description: str
    thumbnails: ThumbnailInfo
    position: int

class ContentDetails(BaseModel):
    videoId: str
    videoPublishedAt: str
class ChartYoutube(BaseModel) :
    snippet: Snippet
    contentDetails: ContentDetails