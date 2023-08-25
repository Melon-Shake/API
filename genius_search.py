import requests
import pandas as pd
from bs4 import BeautifulSoup

GENIUS_API_KEY = "I_rUwBLI1_wEjXSvfEsyHeFK2Bj0V28EG9_6h6FFKR-3rSyGCj8kKWTN7jPmCtcx"


def genius_search(search,GENIUS_API_KEY):     # 노래 id 및 기본 정보 수집
    
    GENIUS_API_KEY = GENIUS_API_KEY


    base_url = "https://api.genius.com"
    headers = {"Authorization": "Bearer " + GENIUS_API_KEY}


    search = search
    search_url = f"{base_url}/search?q={search}"


    response = requests.get(search_url, headers=headers)
    data = response.json()


    if "response" in data and "hits" in data["response"]:
        hits = data["response"]["hits"]
        if hits:
            col = ["ID","Title","artist_names","pyongs_count"]
            a=[]
            for i in data['response']['hits']:
                a.append([i['result']['id'],i['result']['title'],i['result']['artist_names'],i['result']['pyongs_count']])
            return pd.DataFrame(a,columns=col)
    else:
        return "검색 결과를 찾을 수 없습니다."
    
    
def get_lyric(ID,GENIUS_API_KEY):   # 가사 주소 및 앨범 정보 수집
    # Genius API Key
    GENIUS_API_KEY = GENIUS_API_KEY

    # 노래 제목
    ID = ID

    # 검색 요청 보내기
    search_url = f"https://api.genius.com/songs/{ID}"
    headers = {"Authorization": f"Bearer {GENIUS_API_KEY}"}
    response = requests.get(search_url, headers=headers)
    data = response.json()
    return data
    # data['response']['song']['album']['full_title']
    



def genius_lyric_search(url):   # 가사 크롤링
    url = url

    response = requests.get(url)

    if response.status_code == 200:
        page_content = response.content
        soup = BeautifulSoup(page_content, 'html.parser')

        lyrics_containers = soup.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-5')

        lyrics_list = []

        for container in lyrics_containers:
            lyrics_list.extend(container.stripped_strings)

        lyrics = '\n'.join(lyrics_list)
        return lyrics
    else:
        return '페이지를 가져올 수 없습니다.'
    
    
def genius_unique_search(search, GENIUS_API_KEY):   # 종합
    GENIUS_API_KEY = GENIUS_API_KEY
    
    # 노래 id 및 기본 정보
    genius_search_data = genius_search(search, GENIUS_API_KEY)
    ID = genius_search_data.loc[0][0]
    ARTIST = genius_search_data.loc[0][2]
    TITEL = genius_search_data.loc[0][1]
    
    # 가사 주소 및 앨범
    get_lyric_data = get_lyric(ID, GENIUS_API_KEY)['response']['song']
    LYIRC_URL = get_lyric_data['url']
    if get_lyric_data['album'] != None:
        ALBUM = get_lyric_data['album']['name']
    
    #크롤링
    LYRIC = genius_lyric_search(LYIRC_URL)
    print("ID = ",ID)
    print("ARTIST =",ARTIST)
    print("TITEL =",TITEL)
    print("LYIRC_URL =",LYIRC_URL)
    print("ALBUM =",ALBUM)
    print("LYRIC =",LYRIC)