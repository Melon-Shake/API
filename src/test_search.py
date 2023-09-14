import sys
import os
root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
sys.path.append(root_path)
import src.search_spotify as X

search_result = X.search_spotify_by_keywords('아이유')
print(type(search_result.artists))