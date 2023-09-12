
from pydantic import BaseModel

class LoginData(BaseModel):
    email : str
    password : str
    gender : str
    birthdate: str
    mbti : str
    favorite_tracks : str
    favorite_artists : str
    name : str


class Login(BaseModel):
    email:str
    password:str

class Keyword(BaseModel):
    searchInput: str
    email: str  # 사용자 이메일

class search_track(BaseModel):
   email : str
   track_title : str