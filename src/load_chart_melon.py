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
    print(type(song_list)) # <class 'list'>
    print(type(song_list[0])) # <class 'dict'>
    print(song_list[0]) # list[dict]

    test_var= song_list[0].get('ALBUMNAME')
    print(type(test_var))
    print(test_var)
    ##############################################
    testlist = []
    for i in range(len(song_list)):
      song_data = song_list[i].get('ALBUMNAME')
      
      # 값이 none인지 확인
      if song_data is None:
        data_type = "None"
        
      # bool 타임지 확인
      elif isinstance(song_data, bool):
        data_type = "bool"
      
      # int 타입인지 확인
      elif isinstance(song_data, int):
        data_type = "int"
        
      else:
        data_type = "str"
      
      testlist.append(data_type)
      
      data_type_conts = {
        "str":0,
        "int":0,
        "None":0,
        "bool":0,
      }
      
      for item in testlist:
        # data_type = item[1]
        print(item)
        # data_type_conts[data_type] +=1
      # song_data = ChartMelon(**song_list[i])
      # song_data_input= song_data.ALBUMNAME
      # song_data_type= type(song_data.ALBUMNAME)
      # testlist.append((song_data, song_data_type))  
    # print(data_type_conts)
    
    # for i in range(len(song_list)):
    # SONGID 필드만 확인하고 나머지 필드는 무시됩니다.
      # song_data = ChartMelon(SONGID=song_list[i]['SONGID'])
      # song_data_type = type(song_data.SONGID)
      # testlist.append((song_data, song_data_type))
    # print(testlist)

    # x = ChartMelon(**song_list[0])
    # print(len(song_list))

    # print(x.SONGNAME)
    
    
    # for song in song_list :
    #   print(type(song))
    

    # aa =1
    # pared_data = ChartMelon(**song_list)
    # 데이터들
    # chart_melon_result = aa
    
    # for entity in chart_melon_result :
    #   orm = ChartMelonORM(entity.__dict__)
      
    #   with session_scope() as session :
    #     session.add(orm)