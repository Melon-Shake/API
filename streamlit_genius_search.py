import requests
import pandas as pd
from bs4 import BeautifulSoup
import streamlit as st
# https://genius.com/api-clients
GENIUS_API_KEY = "U8Bj95uLfXFHnAkwYV67p1a5tdzmJD7vQSKWMGxi_w_BekWl_gMSLb7sRwl-rI5gqwop8gawaDjzF1mqyYl-6A"

import psycopg2

def is_duplicated_data(artist,album,track):
  # 데이터베이스 연결 정보
  dbname = "postgres"
  user = "postgres"
  password = "12345678"
  host = "database-1.coea55uwjt5p.ap-northeast-1.rds.amazonaws.com"
  port = "5432"

  # 데이터베이스 연결
  conn = psycopg2.connect(
      dbname=dbname,
      user=user,
      password=password,
      host=host,
      port=port
  )

  cursor = conn.cursor()
  query = f"""SELECT *
  FROM route
  WHERE artist_name = '{artist}'
    AND album_name = '{album}'
    AND track_name = '{track}';
  """
  cursor.execute(query)
  result = cursor.fetchall()
  # 커밋
  conn.commit()

  # 연결 종료
  conn.close()
  if result:
    return result # 데이터 삽입 진행
  else:
    return False # 터미널에 우선 추가


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
    return (ID,ARTIST, TITEL, LYIRC_URL, ALBUM, LYRIC)
    # return ("ARTIST =",ARTIST)
    # return ("TITEL =",TITEL)
    # return ("LYIRC_URL =",LYIRC_URL)
    # return ("ALBUM =",ALBUM)
    # return ("LYRIC =",LYRIC)
    
st.title("Genius API 사용")
st.write("영어로 입력해야 결과 더 정확")
st.write("들어간 값이랑 나온 값이랑 교차검증 필요")
artist = st.text_input("가수")
track = st.text_input("제목")

if st.button("가사 검색"):
    search = artist +', '+ track
    data = genius_unique_search(search,GENIUS_API_KEY)
    for i in data:
        st.write(i)
    if is_duplicated_data(artist=data[1],album=data[4],track=data[2]):
        query = f'insert into lyrics (content, track_id genius) values ({data[5]}, ,True)'
    else:
          # 데이터베이스 연결 정보
        dbname = "postgres"
        user = "postgres"
        password = "12345678"
        host = "database-1.coea55uwjt5p.ap-northeast-1.rds.amazonaws.com"
        port = "5432"

        # 데이터베이스 연결
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

        # 커서 생성
        cursor = conn.cursor()

        # # 데이터 삽입
        data_to_insert = (data[2], data[4] , data[1])
        query = "INSERT INTO route (track_name, album_name, artist_name) VALUES (%s, %s, %s)"
        cursor.execute(query, data_to_insert)

        result = cursor.fetchall()
        # 커밋
        conn.commit()

        # 연결 종료
        conn.close()

    # if is_duplicated_data(artist,track)
# if st.button('삽입'):
    

