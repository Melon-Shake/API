from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from lyric import *
app = FastAPI()

GENIUS_API_KEY = "hvNyikfbrRz7IrjRN2wyrFwCc2YstwyCSsxcUAiwg9hbat_vNaEk8nqMBguxrlNt"

class TrackInfo(BaseModel):
    artist: str
    track: str

@app.post("/get_lyrics")
async def get_lyrics(track_info: TrackInfo):
    artist = track_info.artist
    track = track_info.track

    lyrics = lyric_search(artist, track, GENIUS_API_KEY)
    return {"lyrics": lyrics}

def lyric_search(artist, track, GENIUS_API_KEY):
    lyric = musix_match_lyric_search(artist, track)
    if lyric:
        return lyric
    else:
        lyric = genius_unique_search(artist, track, GENIUS_API_KEY)[-1]
        return lyric

def musix_match_lyric_search(artist, track):
    url = 'https://www.musixmatch.com/lyrics/'
    headers = {'User-agent': 'Googlebot'}
    result_url = url + artist + '/' + track

    response = requests.get(result_url, headers=headers)

    if response.status_code == 200:
        page_content = response.content
        soup = BeautifulSoup(page_content, 'html.parser')

        lyrics_container = soup.find_all('span', class_='lyrics__content__ok')

        lyrics_list = []

        for container in lyrics_container:
            lyrics_list.extend(container.stripped_strings)

        lyrics = '\n'.join(lyrics_list)
        return lyrics

@app.post("/insert_lyrics")
async def insert_lyrics(track_info: TrackInfo):
    artist = track_info.artist
    track = track_info.track

    lyrics = lyric_search(artist, track, GENIUS_API_KEY)
    if lyrics:
        insert_data(lyrics, artist, track)
        return {"message": "Lyrics inserted successfully"}
    else:
        return {"message": "Lyrics not found"}

def insert_data(content, artist, track):
    try:
        # Connect to the database and insert data
        # Your database connection and insertion code here
        pass
    except Exception as error:
        return {"error": str(error)}

# Other functions and definitions here (same as provided in your original code)
