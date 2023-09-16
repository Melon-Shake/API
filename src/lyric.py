import requests
import pandas as pd
from bs4 import BeautifulSoup
import psycopg2
import config.db_info as db

GENIUS_API_KEY = "cF1xnE_T3hUohQNUfsTWNR9G-m1nLIfCmN7KrIZKN6LgNzviE_HZHMcQWECqOSMo"

def insert_data(content, track_id,api):
    try:
        connection = psycopg2.connect(**db.db_params)
        cursor = connection.cursor()
        escaped_content = content.replace("'", "''")
        if api == "musix_match":
            query = f"INSERT INTO lyrics (content, id, musix_match) VALUES ('{escaped_content}', '{track_id}', 'True')"
        elif api == "genius":
            query = f"INSERT INTO lyrics (content, id, genius) VALUES ('{escaped_content}', '{track_id}', 'True')"
        cursor.execute(query)

        connection.commit()
        print("데이터가 성공적으로 삽입되었습니다.")

    except (Exception, psycopg2.Error) as error:
        print("데이터 삽입 중 에러 발생:", error)

    finally:
        if connection:
            cursor.close()
            connection.close()

def normalize(url):
    if "Genius-romanizations-" in url:
        new_url = url.replace("Genius-romanizations-","")
        new_url = new_url.replace("romanized-","")
        return new_url
    else:
        return url
        
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
    
def genius_unique_search(artist, track, GENIUS_API_KEY):   # 종합
    GENIUS_API_KEY = GENIUS_API_KEY
    search = artist+', '+track
    # 노래 id 및 기본 정보
    genius_search_data = genius_search(search, GENIUS_API_KEY)
    ID = genius_search_data.loc[0][0]
    ARTIST = genius_search_data.loc[0][2]
    TITEL = genius_search_data.loc[0][1]
    
    # 가사 주소 및 앨범
    get_lyric_data = get_lyric(ID, GENIUS_API_KEY)['response']['song']
    LYIRC_URL = get_lyric_data['url']
    LYIRC_URL = normalize(LYIRC_URL)
    if get_lyric_data['album'] != None:
        ALBUM = get_lyric_data['album']['name']
    
        #크롤링
        LYRIC = genius_lyric_search(LYIRC_URL)
        return (ID,ARTIST, TITEL, LYIRC_URL, ALBUM, LYRIC)
    else:
        LYRIC = genius_lyric_search(LYIRC_URL)
        return (ID,ARTIST, TITEL, LYIRC_URL, LYRIC)
    
def musix_match_lyric_search(artist,track):
    url = 'https://www.musixmatch.com/lyrics/'
    headers = {'User-agent': 'Googlebot'}
    result_url = url + artist + '/' + track

    response = requests.get(result_url, headers=headers)

    if response.status_code == 200 :
        page_content = response.content
        soup = BeautifulSoup(page_content, 'html.parser')

        # 가사부분class를 find_all 받으면 list형태
        lyrics_container = soup.find_all('span', class_='lyrics__content__ok')

        lyrics_list = []

        for container in lyrics_container:
            lyrics_list.extend(container.stripped_strings)

        lyrics = '\n'.join(lyrics_list)
        return lyrics

def lyric_search(artist, track, GENIUS_API_KEY):
    lyric = musix_match_lyric_search(artist,track)
    if lyric:
        print("musix_match")
        return lyric
    else:
        print("genius")
        return genius_unique_search(artist,track,GENIUS_API_KEY)[-1] 
    
def lyric_search_and_input(artist, track, track_id, GENIUS_API_KEY):
    lyric = musix_match_lyric_search(artist,track)
    if lyric:
        api = "musix_match"
        insert_data(lyric,track_id,api)
        return True
    else:
        api = "genius"
        lyric = genius_unique_search(artist,track,GENIUS_API_KEY)[-1] 
        insert_data(lyric,track_id,api)
        return True

# artist = "(여자) 아이들"
# track = "All Night"
# print(lyric_search(artist,track,GENIUS_API_KEY))
