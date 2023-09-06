import requests

if __name__ == '__main__' :
    response = requests.post('https://app.genie.co.kr/chart/j_RealTimeRankSongList.json'
                             ,headers={
                                 'Content_Type' : 'application/x-www-form-urlencoded'
                             }
                             ,data={
                                 'dict': 'R'
                                 ,'pg_size': '200'
                             }
                            )

    if response.status_code == 200 :
        responsed_data = response.json()
        arr = responsed_data.get('DataSet').get('DATA')
        
        print(len(arr))
        print(arr[0])        
        
        for a in arr :
            pass

    else : print(response.status_code)