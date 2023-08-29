from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from lyric import *
app = FastAPI()


GENIUS_API_KEY = "hvNyikfbrRz7IrjRN2wyrFwCc2YstwyCSsxcUAiwg9hbat_vNaEk8nqMBguxrlNt"

class input_data(BaseModel):
    artist : str
    track : str
    track_id : int
    GENIUS_API_KEY : str

@app.post("/lyric_input/")
def lyric_input(item : input_data):
    artist = item.artist
    track = item.track
    track_id = item.track_id
    GENIUS_API_KEY = item.GENIUS_API_KEY
    result = lyric_search_and_input(artist,track,track_id,GENIUS_API_KEY)
    if result:
        return {"result" : f"Lyrics have been added to track_id : {track_id}"}
    else:
        raise HTTPException(status_code=404, detail="Lyric ERR.")