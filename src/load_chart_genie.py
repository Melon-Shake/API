import requests

if __name__ == '__main__' :
    response = requests.get('')

    if response.status_code == 200 :
        pass
    
    else : print(response.status_code)