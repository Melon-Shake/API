import requests
import pandas as pd
import streamlit as st
from musixmatch import Musixmatch
from bs4 import BeautifulSoup


# apikey = '0140decf9ddfc9e2f5056cb6775fa493'

#curl 구성
url = 'https://www.musixmatch.com/lyrics/'
headers = {'User-agent': 'Googlebot'}
artist_name = st.text_input('가수이름')
track_name = st.text_input('노래제목')

# 검색버튼을 누르면 입력받은 '가수/노래제목' 으로 가사 크롤링
if st.button('검색'):
    result_url = url + artist_name + '/' + track_name
    
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
        st.write(lyrics)
        
        
    else:
        st.write(result_url)
        st.write(response.status_code)
