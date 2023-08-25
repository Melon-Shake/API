import requests
import pandas as pd
import streamlit as st
from musixmatch import Musixmatch
from bs4 import BeautifulSoup

apikey = '0140decf9ddfc9e2f5056cb6775fa493'

# musixmatch = Musixmatch(apikey)
# celebrity = musixmatch.track_lyrics_get(212057015)
# print(celebrity)

url = 'https://www.musixmatch.com/lyrics/'
headers = {'User-agent': 'Googlebot'}
artist_name = st.text_input('가수이름')
track_name = st.text_input('노래제목')
if st.button('검색'):
    result_url = url + artist_name + '/' + track_name

    response = requests.get(result_url, headers=headers)

    if response.status_code == 200 :
        page_content = response.content
        soup = BeautifulSoup(page_content, 'html.parser')
        
        # lyrics_container = soup.find_all('span', __build_class__='lyrics__content__ok')
        lyrics_container = soup.find_all('span', class_='lyrics__content__ok')

        st.write(lyrics_container)
    else:
        st.write(result_url)
        st.write(response.status_code)
