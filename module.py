import requests

# AuthToken 읽기
def read_AuthToken_from_file():
    try:
        with open("config/AuthToken.txt", "r") as file:
            token = file.read().strip()
            return token
    except FileNotFoundError:
        return None
# RefreshToken 읽기
def read_RefreshToken_from_file():
    try:
        with open("config/RefreshToken.txt", "r") as file:
            token = file.read().strip()
            return token
    except FileNotFoundError:
        return None
    
