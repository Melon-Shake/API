from model.database import session_scope

import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)

from model.chart_melon import ChartMelon, MelonORM
import  requests

if __name__ == '__main__':
  _APP_VERSION = "6.5.8.1"
  _CP_ID = "AS40"
  _USER_AGENT = f"{_CP_ID}; Android 13; {_APP_VERSION}; sdk_gphone64_arm64"
  _CHART_API_URL = f"https://m2.melon.com/m6/chart/ent/songChartList.json?cpId={_CP_ID}&cpKey=14LNC3&appVer={_APP_VERSION}"
  headers = {"User-Agent": _USER_AGENT}
  
  response = requests.get(_CHART_API_URL,headers=headers)
  
  if response.status_code == 200 :
    response_data = response.json()
    song_list = response_data['response']['SONGLIST']
    for item in song_list:
      entity = ChartMelon(**item)
      orm = MelonORM(entity)

      with session_scope() as session :
        session.add(orm)