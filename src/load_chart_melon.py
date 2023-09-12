import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.database import session_scope
from model.chart_melon import ChartMelon, MelonORM
import requests

if __name__ == '__main__':
  _APP_VERSION = "6.5.8.1"
  _CP_ID = "AS40"
  _USER_AGENT = f"{_CP_ID}; Android 13; {_APP_VERSION}; sdk_gphone64_arm64"
  _CHART_API_URL = f"https://m2.melon.com/m6/chart/ent/songChartList.json?cpId={_CP_ID}&cpKey=14LNC3&appVer={_APP_VERSION}"
  headers = {"User-Agent": _USER_AGENT}
  
  response = requests.get(_CHART_API_URL,headers=headers)
  
  if response.status_code == 200 :
    response = response.json()
    responsed_data = response['response']['SONGLIST']
    
    entries = {}
    for itme in responsed_data:
        for index, item in enumerate(responsed_data):
            track_title = item['SONGNAME']
            album_title = item['ALBUMNAME']
            artists = item.get('ARTISTLIST')
            artist_pre = []
            for artist in artists:
                artist_nm = artist['ARTISTNAME']
                artist_pre.append(artist_nm)
            entries[index+1] = [track_title, artist_pre, album_title]
    # for item in song_list:
    #   entity = ChartMelon(**item)
    #   orm = MelonORM(entity)

    #   with session_scope() as session :
    #     session.add(orm)