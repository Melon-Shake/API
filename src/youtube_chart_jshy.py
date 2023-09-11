from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import re
import json
from urllib.parse import urlparse, parse_qs
import requests
import config.youtubekey as youtube
import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
from model.ytmusic import js_ChartYoutube, Response, hy_ChartYoutube, js_SumChart


# Lucete youtube top100 크롤링
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
    changes = []
    views = []
    pre_ranks = []
    urls = []
    video_ids =  []
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
        
        craw_changes = div_element.find_all('div', class_ = 'views-change-cell style-scope ytmc-chart-table')
        for change in craw_changes:
            changes.append(change.get_text().strip())
            
        craw_views = div_element.find_all('div', class_ = 'views-cell style-scope ytmc-chart-table')
        for view in craw_views:
            views.append(view.get_text().strip())
            
        previous = div_element.find_all('div', class_ = 'previous-rank style-scope ytmc-chart-table')
        for view in previous:
            text = view.get_text().strip()
            try:
                match = (re.search(r'#(\d+)', text)).group(1)
            except:
                match = None
            pre_ranks.append(match)

        craw_urls = div_element.find_all('img', class_='chart-entry-thumbnail clickable style-scope ytmc-chart-table')
        for url in craw_urls:
            ep = url.get('endpoint')
            url_data = json.loads(ep)
            full_url = url_data['urlEndpoint']['url']
            urls.append(full_url)
            url_parts = urlparse(full_url)
            query_params = parse_qs(url_parts.query)
            video_id = query_params.get('v', [''])[0]
            video_ids.append(video_id)

    rank_const.pop(0)
    changes.pop(0)
    views.pop(0)
    # df = pd.DataFrame({'Title': titles, 'Artist': artists, 'Rank_const': rank_const, 'Change':changes, 'View':views, 'Previous_rank':pre_ranks, 'Url':urls, 'Video_ID':video_ids})
    driver.quit()
    
    youtube_chart = [{'title': title,'artist': artist ,'rank_const': rank_const, 'change':change, 'view':view, 'previous_rank':pre_rank, 'url':url, 'video_Id':video_id} for title, artist, rank_const, change, view, pre_rank, url, video_id in zip(titles,artists,rank_const,changes,views,pre_ranks,urls,video_ids)]
    response = {'args':youtube_chart}
    
    x = Response(**response)
    return x
    
def yt_craw_start(weeks_ago : int):
    past_week = yt_get_weeks()
    start_date = past_week[weeks_ago][0]
    end_date = past_week[weeks_ago][1]
    weeks_ago -=1
    if weeks_ago == -1:
        url = 'https://charts.youtube.com/charts/TopSongs/kr?hl=ko'
    else:
        url = f"https://charts.youtube.com/charts/TopSongs/kr/{start_date}-{end_date}?hl=ko"
    x = yt_craw(url)
    return x

hy_chart = yt_craw_start(0)

# ssg youtube api ---------------------------------------------------------------------------------------
key= youtube.key

url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet%2C%20contentDetails&maxResults=100&playlistId=PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m&key={key}'

response = requests.get(url)

if response.status_code == 200:
    response_json = response.json()
    next_page_token = response_json['nextPageToken']
    # print(next_page_token)
    playlist_item = response_json.get('items')
    youtube_args1 = []
    # print(type(playlist_item[0]['contentDetails']['videoPublishedAt']))
    for item in playlist_item : 
        youtube_item = js_ChartYoutube(**item)
        # print(youtube_item)
        youtube_args1.append(youtube_item)
        
        
    url2 = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet%2C%20contentDetails&maxResults=100&pageToken={next_page_token}&playlistId=PL4fGSI1pDJn6jXS_Tv_N9B8Z0HTRVJE0m&key={key}'
    response2 = requests.get(url2)
    
    response2_json = response2.json()
    playlist_item2 = response2_json.get('items')
    
    youtube_args2 = []
    for item2 in playlist_item2:
        # print(item2.get('contentDetails'))
        youtube_item2 = js_ChartYoutube(**item2)
        youtube_args2.append(youtube_item2)
        # print(youtube_item2)
        # print(type(youtube_item2))
else:
    print('error_code ='+ response.status_code)

result_item = youtube_args1+youtube_args2
result_chart = js_SumChart(result_item=result_item)

total_youtube_chart = {'all':[]}

for i in range(100):
    combined_item = (hy_chart.args[i],result_chart.result_item[i])
    total_youtube_chart['all'].append(combined_item)

print(total_youtube_chart['all'])
