import json, sys, requests
from datetime import datetime
from urllib.parse import unquote


_CONTENT_TYPE = "application/x-www-form-urlencoded"
_REALTIME_CHART_API_URL = "https://app.genie.co.kr/chart/j_RealTimeRankSongList.json"
# _ALLTIME_CHART_API_URL = "https://app.genie.co.kr/chart/j_RankSongListAlltime.json"
# _CHART_API_URL = "https://app.genie.co.kr/chart/j_RankSongList.json"

class GenieChartPeriod:
    Realtime = 'R'
    Alltime = 'A'
    Daily = 'D'
    Weekly = 'W'
    Monthly = 'M'
    
headers = {'Content_Type': _CONTENT_TYPE}

# chart_period = GenieChartPeriod.Realtime

# if self.chart_period != GenieChartPeriod.Realtime and chart_period != GenieChartPeriod.Alltime:
data = {
  'pgSize' : '100'
  }

url = _REALTIME_CHART_API_URL

res = requests.post(
  url,
  headers=headers,
  data=data
)
result = res.json()
# json.dumps(result, indent=4, ensure_ascii=True)
print(len(result['DataSet']['DATA']))
# result
