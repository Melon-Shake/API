from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urlparse, parse_qs
def gg_lyrics_craw(artist,track,album=''):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  


    driver = webdriver.Chrome(options=chrome_options)

    url = f"https://www.google.com/search?q={artist}+{track}+{album}+lyrics&sca_esv=565545338&ei=adsDZcrGD_nY1e8P8NC1yAQ&ved=0ahUKEwiKn8vV4auBAxV5bPUHHXBoDUkQ4dUDCBA&uact=5&oq={artist}+{track}+{album}+lyrics&gs_lp=Egxnd3Mtd2l6LXNlcnAiH-yVhOydtOycoCDsoovsnYDrgqAgUkVBTCBseXJpY3MyCBAhGKABGMMEMggQIRigARjDBDIIECEYoAEYwwQyCBAhGKABGMMESLAjULMIWIwccAJ4AZABAJgBlwGgAZgFqgEDMC41uAEDyAEA-AEBwgIKEAAYRxjWBBiwA8ICBBAAGB7iAwQYACBBiAYBkAYK&sclient=gws-wiz-serp"

    driver.get(url)
    # time.sleep(10)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')

    articles = soup.find_all('div', class_='sATSHe')
    lyrics_list = []
    for div in articles:
        vals = div.find_all('div', class_='ujudUb')
        for val in vals:
            lyrics_list.append(val.text)
    return lyrics_list