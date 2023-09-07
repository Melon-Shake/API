from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
from model.hy_ytmusic import ChartYoutube, Response

driver = webdriver.Chrome()

url = f"https://charts.youtube.com/charts/TopSongs/kr?hl=ko"

driver.get(url)
time.sleep(10)
# JavaScript가 실행되는 것을 기다림 (예: 10초 동안 기다림)
# wait = WebDriverWait(driver, 10)
# wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ytmc-ellipsis-text-container style-scope ytmc-ellipsis-text')))
req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

articles = soup.find_all('div',class_ = 'title-cell style-scope ytmc-chart-table')
# print(articles)
youtube_chart = {}
# 두 개씩 끊어서 저장할 리스트
titles = []
artists = []

# ResultSet 내에서 값을 추출
for div_element in articles:
    # 각 div 요소에서 원하는 값을 찾음
    divs = div_element.find_all('div', class_='hidden style-scope paper-tooltip')

    
    # divs에 두 개의 요소가 있는지 확인하고 추출
    if len(divs) == 2:
        title = divs[0].get_text().strip()  # strip()를 사용하여 앞뒤 공백 제거
        artist = divs[1].get_text().strip()  # strip()를 사용하여 앞뒤 공백 제거
        # 리스트에 추가
        titles.append(title)
        artists.append(artist)

youtube_chart = [{'title': title,'artist': artist} for title, artist in zip(titles,artists)]

# 아항, 아까 Response 라는 pydantic 모델에서 받아내려면, 리턴의 형태가 딕셔너리여야 해서 args 로 넣으려고 했던 거구나? 
# 아무튼 이렇게 해결
response = {'args':youtube_chart}
x = Response(**response)
print(x)

    
# for i in range(len(titles)):
#     youtube_chart = {'title':titles[i],
#                     'artist':artists[i]}
#     x = ChartYoutube(**youtube_chart)
#     # print(type(x))
#     print(x.title)


# print(youtube_chart)



# playlist_item = youtube_chart.get('items')
        
#     for item in playlist_item:
#         youtube_item = ChartYoutube(**item)
#         print(youtube_item)


# 추출한 데이터를 Pandas DataFrame으로 변환
# df = pd.DataFrame({'Title': titles, 'Artist': artists})

# 결과 출력
# print(df)
 