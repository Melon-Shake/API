from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import re
import json
from urllib.parse import urlparse, parse_qs
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
from model.hy_ytmusic import ChartYoutube, Response

def yt_get_weeks():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  

    driver = webdriver.Chrome(options=chrome_options)

    url = "https://charts.youtube.com/charts/TopSongs/kr?hl=ko"

    driver.get(url)
    time.sleep(10)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')

    articles = soup.find_all('div', class_='period-selector style-scope ytmc-charts')
    for article in articles:
        a = article.find_all('paper-item', class_='style-scope ytmc-dropdown')
        result = []
        for item in a:
            option_id = item['option-id']
            # print(option_ids)
            # 정규 표현식 패턴
            pattern = r'weekly:(\d+):(\d+):kr'

            # 숫자 값을 추출하여 튜플로 저장

            match = re.match(pattern, option_id)
            if match:
                start_date = int(match.group(1))
                end_date = int(match.group(2))
                result.append((start_date, end_date))

        return result
    
    
def yt_craw(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  
    driver = webdriver.Chrome(options=chrome_options)

    url = url

    driver.get(url)
    time.sleep(10)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')

    articles = soup.find_all('div',class_ = 'chart-table style-scope ytmc-chart-table')
    titles = []
    artists = []
    rank_const = []
    CHANGE = []
    VIEWS = []
    PRE_RANK = []
    URL = []
    VIDEO_ID =  []
    # ResultSet 내에서 값을 추출
    for div_element in articles:
        # 각 div 요소에서 원하는 값을 찾음
        divs = div_element.find_all('div', class_='hidden style-scope paper-tooltip')
        for i, div in enumerate(divs):
            text = div.get_text(strip=True)  # 텍스트 추출 및 공백 제거
            if i % 2 == 0:
                titles.append(text)
            else:
                artists.append(text)
        consts = div_element.find_all('div', class_='chart-period-cell style-scope ytmc-chart-table')
        # print(consts.get_text().strip())
        for const in consts:
            rank_const.append(const.get_text().strip())
        
        changes = div_element.find_all('div', class_ = 'views-change-cell style-scope ytmc-chart-table')
        for change in changes:
            CHANGE.append(change.get_text().strip())
            
        views = div_element.find_all('div', class_ = 'views-cell style-scope ytmc-chart-table')
        for view in views:
            VIEWS.append(view.get_text().strip())
            
        previous = div_element.find_all('div', class_ = 'previous-rank style-scope ytmc-chart-table')
        for view in previous:
            text = view.get_text().strip()
            try:
                match = (re.search(r'#(\d+)', text)).group(1)
            except:
                match = None
            PRE_RANK.append(match)

        urls = div_element.find_all('img', class_='chart-entry-thumbnail clickable style-scope ytmc-chart-table')
        for url in urls:
            ep = url.get('endpoint')
            url_data = json.loads(ep)
            full_url = url_data['urlEndpoint']['url']
            URL.append(full_url)
            url_parts = urlparse(full_url)
            query_params = parse_qs(url_parts.query)
            video_id = query_params.get('v', [''])[0]
            VIDEO_ID.append(video_id)

    VIEWS.pop(0)
    CHANGE.pop(0)
    rank_const.pop(0)
    df = pd.DataFrame({'Title': titles, 'Artist': artists, 'Rank_const': rank_const, 'Change':CHANGE, 'View':VIEWS, 'Previous_rank':PRE_RANK, 'Url':URL, 'Video_ID':VIDEO_ID})
    driver.quit()
    return df
    
def yt_craw_start(weeks_ago : int):
    past_week = yt_get_weeks()
    start_date = past_week[weeks_ago][0]
    end_date = past_week[weeks_ago][1]
    weeks_ago -=1
    if weeks_ago == -1:
        url = 'https://charts.youtube.com/charts/TopSongs/kr?hl=ko'
    else:
        url = f"https://charts.youtube.com/charts/TopSongs/kr/{start_date}-{end_date}?hl=ko"
    df = yt_craw(url)
    return df

yt_chart = yt_craw_start(1)
print(yt_chart)