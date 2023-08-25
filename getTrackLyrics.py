import requests
import pandas as pd
from musixmatch import Musixmatch

apikey = '0140decf9ddfc9e2f5056cb6775fa493'

musixmatch = Musixmatch(apikey)

celebrity = musixmatch.track_lyrics_get(212057015)

print(celebrity)