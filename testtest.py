import json
import sys
import urllib.parse
from datetime import datetime

import requests

_USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
_ACCEPT = "application/json"
_CHART_API_URL = "https://apis.naver.com/vibeWeb/musicapiweb/vibe/v1/chart/track/total"


class VibeChartRequestException(Exception):
    pass


class VibeChartParseException(Exception):
    pass


class VibeChartQueryException(Exception):
    pass


class ChartEntry:
    """Represents an entry on a chart.
    Attributes:
        title: The title of the track
        artist: The name of the artist.
        image: The URL of the cover image for the track
        lastPos: The track's last position on the previous period.
        rank: The track's current rank position on the chart.
        isNew: Whether the track is new to the chart.
    """

    def __init__(self, title: str, artist: str, image: str, lastPos: int, rank: int, isNew: bool):
        self.title = title
        self.artist = artist
        self.image = image
        self.lastPos = lastPos
        self.rank = rank
        self.isNew = isNew

    def __repr__(self):
        return "{}.{}(title={!r}, artist={!r})".format(
            self.__class__.__module__, self.__class__.__name__, self.title, self.artist
        )

    def __str__(self):
        """Returns a string of the form 'TITLE by ARTIST'."""
        if self.title:
            s = u"'%s' by %s" % (self.title, self.artist)
        else:
            s = u"%s" % self.artist

        if sys.version_info.major < 3:
            return s.encode(getattr(sys.stdout, "encoding", "") or "utf8")
        else:
            return s

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)


class ChartData:
    """Represents a particular Bugs chart by a particular period.
    Attributes:
        name: The chart name
        date: The chart date
        queryStart: The starting index of the chart entries to be retrieved from the Vibe API. (default: 1)
        queryCount: The number of items to retrieve from the API response, starting from `queryStart`. (default: 100)
        imageSize: The size of cover image for the track. (default: 256)
        fetch: A boolean value that indicates whether to retrieve the chart data immediately. If set to `False`, you can fetch the data later using the `fetchEntries()` method.
    """

    def __init__(self, queryStart: int = 1, queryCount: int = 100, imageSize: int = 256, fetch: bool = True):
        self.maxQueryCount = 0
        self.queryStart = queryStart
        self.queryCount = queryCount
        self.imageSize = imageSize
        self.entries = []

        if fetch:
            self.fetchEntries()

    def __getitem__(self, key):
        return self.entries[key]

    def __len__(self):
        return len(self.entries)

    def json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)

    def fetchEntries(self):
        headers = {
            "User-Agent": _USER_AGENT,
            "Accept": _ACCEPT
        }

        if 0 < self.maxQueryCount < (self.queryCount + self.queryStart - 1):
            raise VibeChartQueryException(f"Exceeded maximum query limit. (limit: {self.maxQueryCount})")

        res = requests.get(
            f"{_CHART_API_URL}?start={self.queryStart}&display={self.queryCount}",
            headers=headers
        )

        if res.status_code != 200:
            message = f"Request has been failed. {res.status_code}"
            raise VibeChartRequestException(message)

        data = res.json()

        self._parseEntries(data)

    def _parseEntries(self, data):
        try:
            c_data = data['response']['result']['chart']
            self.name = c_data['title']
            self.date = self._parseDate(c_data['date'])
            self.maxQueryCount = int(c_data['chartTotalCount'])

            for item in c_data['items']['tracks']:
                entry = ChartEntry(
                    title=item['trackTitle'],
                    artist=item['artists'][0]['artistName'],
                    image=self._getResizedImageUrl(item['album']['imageUrl']),
                    rank=int(item['rank']['currentRank']),
                    lastPos=0,
                    isNew=item['rank']['isNew']
                )
                entry.lastPos = entry.rank + int(item['rank']['rankVariation'])
                self.entries.append(entry)

        except Exception as e:
            raise VibeChartParseException(e)

    def _parseDate(self, timestamp_ms):
        timestamp_s = timestamp_ms / 1000
        return datetime.utcfromtimestamp(timestamp_s)

    def _getResizedImageUrl(self, url):
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        query_params['type'] = f'r{self.imageSize}Fll'

        new_query_string = urllib.parse.urlencode(query_params, doseq=True)
        return urllib.parse.urlunparse(
            (parsed_url.scheme, parsed_url.netloc, parsed_url.path,
             parsed_url.params, new_query_string, parsed_url.fragment)
        )