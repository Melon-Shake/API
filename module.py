import requests
import string

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
# 영문포함 검사
def has_non_english_characters(text):
    for char in text:
        if char not in string.printable or char in string.ascii_letters:
            return True
    return False
    
