from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from lyric import *
from sp_track import *
app = FastAPI()


# GENIUS_API_KEY = "U1RN70QWau9zk3qi3BPn_A-q4Bft_3jnw8uLBp2lVafQgOQiA_kjSEyxzr88eI9d"

class lyric_data(BaseModel):
    artist : str
    track : str
    track_id : int
    GENIUS_API_KEY : str = "U1RN70QWau9zk3qi3BPn_A-q4Bft_3jnw8uLBp2lVafQgOQiA_kjSEyxzr88eI9d"

class sp_data(BaseModel):
    artist : str
    album : str
    track : str
    
    
@app.get("/")
def hello():
    return {"result":"hi"}

@app.post("/lyric_input/")
def lyric_input(item : lyric_data):
    artist = item.artist
    track = item.track
    track_id = item.track_id
    GENIUS_API_KEY = item.GENIUS_API_KEY
    result = lyric_search_and_input(artist,track,track_id,GENIUS_API_KEY)
    if result:
        return {"result" : f"Lyrics have been added to track_id : {track_id}"}
    else:
        raise HTTPException(status_code=404, detail="Lyric ERR.")
    
@app.post("/sp_and_track_update/")
def sp_track_input(item: sp_data):
    artist = item.artist
    album = item.album
    track = item.track
    d = get_sp_track_id(artist, album, track)
    
    if d[0] is not None and d[1] is not None:  # get_sp_track_id 함수의 반환값이 None이 아닌지 확인
        result = sp_and_track_input(d[0], d[1], artist, album, track)
        return result
    else:
        raise HTTPException(status_code=404, detail="Track not found or error in processing.")


    
# @app.post("/sp_and_track_update/")
# def sp_track_input(item : sp_data):
#     artist = item.artist
#     album = item.album
#     track = item.track
#     d = get_sp_track_id(artist, album, track)
#     print(d)
#     result = sp_and_track_input(d[0],d[1],artist, album, track)
#     return result
    
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)