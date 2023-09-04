import json
import sys
from datetime import datetime
import requests

_USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36"
_IMAGE_PREFIX_URL = "https://image.bugsm.co.kr/album/images"
_CHART_API_URL = "https://m.bugs.co.kr/api/getChartTrack"


class BugsChartType:
    All = 20151
    Domestic = 20152
    International = 20153


class BugsChartPeriod:
    Realtime = 'realtime'
    Daily = 'day'
    Weekly = 'week'


class BugsChartRequestException(Exception):
    pass


class BugsChartParseException(Exception):
    pass


class ChartEntry:
    """Represents an entry on a chart.
    Attributes:
        title: The title of the track
        artist: The name of the artist.
        image: The URL of the cover image for the track
        peakPos: The track's peak position on the chart.
        lastPos: The track's last position on the previous period.
        rank: The track's current rank position on the chart.
    """

    def __init__(self, title: str, artist: str, image: str, peakPos: int, lastPos: int, rank: int):
        self.title = title
        self.artist = artist
        self.image = image
        self.peakPos = peakPos
        self.lastPos = lastPos
        self.rank = rank

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
        date: The chart date.
        chartType: The chart type.
        chartPeriod: The period for the chart.
        imageSize: The size of cover image for the track. (default: 256)
        fetch: A boolean value that indicates whether to retrieve the chart data immediately. If set to `False`, you can fetch the data later using the `fetchEntries()` method.
    """

    def __init__(self, chartType: BugsChartType = BugsChartType.All,
                 chartPeriod: BugsChartPeriod = BugsChartPeriod.Realtime, imageSize: int = 256,
                 fetch: bool = True):
        self.chartType = chartType
        self.chartPeriod = chartPeriod
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
            "User-Agent": _USER_AGENT
        }

        data = {
            "period_tp": self.chartPeriod,
            "svc_type": self.chartType,
            "size": 100,
        }

        res = requests.post(
            _CHART_API_URL,
            headers=headers,
            data=data
        )

        if res.status_code != 200:
            message = f"Request is invalid. response status code={res.status_code}"
            raise BugsChartRequestException(message)

        data = res.json()
        if int(data.get('ret_code')) > 0:
            message = f"Request is invalid. response message=${data.get('ret_msg')}"
            raise BugsChartRequestException(message)

        self._parseEntries(data)

    def _parseEntries(self, data):
        try:
            self.date = self._parseDate(int(data['info']['end_dt']))
            list = data['list']
            for item in list:
                entry = ChartEntry(
                    title=item['track_title'],
                    artist=item['artists'][0]['artist_nm'],
                    image=f"{_IMAGE_PREFIX_URL}/{self.imageSize}{item['album']['image']['path']}",
                    rank=int(item['list_attr']['rank']),
                    peakPos=int(item['list_attr']['rank_peak']),
                    lastPos=int(item['list_attr']['rank_last']),
                )
                self.entries.append(entry)
        except Exception as e:
            raise BugsChartParseException(e)

    def _parseDate(self, timestamp_ms):
        timestamp_s = timestamp_ms / 1000
        return datetime.utcfromtimestamp(timestamp_s)