# 기사 제목 받아오기
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

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

# 추출한 데이터를 Pandas DataFrame으로 변환
df = pd.DataFrame({'Title': titles, 'Artist': artists})

# 결과 출력
print(df)
 