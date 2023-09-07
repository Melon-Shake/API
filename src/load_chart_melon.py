from model.database import session_scope
# from model.chart_melon import ChartMelonORM
from model.melon_api import ChartMelon
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
      parsed_data = ChartMelon(**item)
      print(type(parsed_data))