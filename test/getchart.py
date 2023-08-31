import datetime
import json
import re
import sys
import warnings

from bs4 import BeautifulSoup
import requests

# add variable
_TARGET_SITE = "https://www.billboard.com"

# defaut variable
_APP_VERSION = "6.5.8.1"
_CP_ID = "AS40"
_USER_AGENT = f"{_CP_ID}; Android 13; {_APP_VERSION}; sdk_gphone64_arm64"
_CHART_API_URL = f"https://m2.melon.com/m6/chart/ent/songChartList.json?cpId={_CP_ID}&cpKey=14LNC3&appVer={_APP_VERSION}"

# css selector constants
_CHART_NAME_SELECTOR = 'meta[property="og:title"]'
_DATE_ELEMENT_SELECTOR = "button.chart-detail-header__date-selector-button"
_PREVIOUS_DATE_SELECTOR = "span.fa-chevron-left"
_NEXT_DATE_SELECTOR = "span.fa-chevron-right"
_ENTRY_LIST_SELECTOR = "div.chart-list-item"
_ENTRY_TITLE_ATTR = "data-title"
_ENTRY_ARTIST_ATTR = "data-artist"
_ENTRY_IMAGE_SELECTOR = "img.chart-list-item__image"
_ENTRY_RANK_ATTR = "data-rank"

# constants for the getMinistatsCellValue helper function
_MINISTATS_CELL = "div.chart-list-item__ministats-cell"
_MINISTATS_CELL_HEADING = "span.chart-list-item__ministats-cell-heading"

class BillboardNotFoundException(Exception):
    pass

class BillboardParseException(Exception):
    pass

class UnsupportedYearWarning(UserWarning):
    pass

class ChartEntry:
  """차트에 있는 항목을 나타냅니다(일반적으로 단일 트랙).
  
    속성:
      title(string): 트랙의 제목
      artist(string): 5개 사의 형식화된 대로 트랙 아티스트의 이름
              여러 아티스트나 피처링된 아티스트가 있는 경우, 문자열에 포함
      image(string) : 트랙의 이미지 URL 
      peakPos(int): 차트 날짜를 기준으로 한 차트와 최고 순위(이 정보가 포함되지 않는 경우 none)
      lastPos(int): 이전 주 순위, 이전 주 차트에 없는 경우 0(이 정보가 포함되지 않는 경우 none)
      weeks: 차트에 들어온 기간을 weeks로 표기(주 단위로)
      rank(int): 현재 차트 순위.
      isNew(bool): 음악이 차트에 처음 등장했는지 여부
      
  """
  def __init__(self, title, artist, image, peakPos, lastPos, weeks, rank, isNew):
    self.title = title
    self.artist = artist
    self.image = image
    self.peakPos = peakPos
    self.lastPos = lastPos
    self.weeks = weeks
    self.rank = rank
    self.isNew = isNew
  
  def __repr__(self):
    return f"{self.__class__.__module__}.{self.__class__.__name__}(title={self.title!r}, aritst={self.artist!r})"
  
  def __str__(self):
    """제목을 문자열로 리턴"""
    if self.title:
      s = f"'{self.title}' by {self.artist}"
    else:
      s = f"{self.artist}"
      
    if sys.version_info.major < 3:
      return s.encode(getattr(sys.stdout, "encoding", "") or "utf8")
    else:
      return s
      
  def json(self):
    """json 형태로 반환"""
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class ChartData:
  def __init__(self, name, date=None, year=None, fetch=True, max_retries=5, timeout=25):
    """차트데이터 생성

    Args:
        name (string): 차트의 이름 ex "TOP100" or "HOT100"
        date (string): 날짜 데이터 입니다. 문자열로 "YYYY-MM-DD" 표기합니다.
                      기본적으로 최신 날짜를 지원하지만 유효하지 않는 날짜인 경우 가장 가까운 차트일로 반올림하여 처리됩니다.
        year (string): 연말 차트를 요청할 때 사용하는 인자로, YYYY 형식의 연도를 문자열로 제공해야 합니다.
                        date와 year 중 하나만 제공할 수 있습니다.
        fetch (bool):  차트 데이터를 즉시 Billboard.com에서 가져올지 여부를 나타내는 불리언 값입니다. 
                      만약 False로 설정하면 fetchEntries() 메서드를 사용하여 나중에 데이터를 가져올 수 있습니다.
        maxretries (int): 데이터를 요청할 때 최대 재시도 횟수를 나타냅니다. 기본값은 5입니다.
        timeout (int): 서버 응답을 기다릴 최대 시간(초 단위)을 나타냅니다. None인 경우 제한 시간이 없습니다.
    """
    self.name = name
    
    if sum(map(bool, [date, year])) >=2 :
      raise ValueError("Can't supply both `date` and `year`.")
    
    if date is not None:
      if not re.match(r"\d{4}-\d{2}-\{2}", str(date)):
        raise ValueError("date args is not in YYYY-MM-DD")
      try:
        datetime.datetime(*(int(x) for x in str(date).split("-")))
      except:
        raise ValueError("date argument is in invalid")
      
      if year is not None:
        if not re.match(r"\d{4}", str(year)):
          raise ValueError("year argument is not in YYYY format")
        
      self.date = date
      self.year = year
      self.title = ""
      
      self._max_retries = max_retries
      self._timeout = timeout
      
      self.entries = []
      if fetch:
        self.fetchEntries()
        
  def __repr__(self):
    if self.year:
      return f"{self.__class__.__module__},{self.__class__.__name__}({self.name!r}, year={self.year!r})"
    return f"{self.__class__.__module__}, {self.__class__.__name__}({self.name!r}, year={self.date!r})"
    
  def __str__(self):
    """차트를 사람이 읽을수 있게 문자열로 반환"""
    if self.year:
      s = f"{self.name} chart ({self.year})"
    elif not self.date:
      s = f"{self.name}"
    else:
      s = f"{self.name} chart from {self.date}"
    s += "\n" +"-" *len(s)
    for n, entry in enumerate(self.entries):
      s += f"\n{entry.rank}. {str(entry)}"
    return s
    
  def __getitem__(self, key):
    """(key +1)번째 차트 항목을 반환합니다.

    Args:
        key (_type_): _description_
    """
    return self.entries[key]
  def __len__(self):
    """차트 엔트리(항목)의 개수를 반환, 길이가 0이라면 잘못된 요청"""
    return len(self.entries)
  
  def json(self):
    """문자열 json으로 반환"""
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent = 4)
  
  def _parsePage(self, soup):
    chartTitleElement = soup.select_one(_CHART_NAME_SELECTOR)
    if chartTitleElement:
      self.title = re.sub(
        " Chart$",
        "",
        chartTitleElement.get("content", "").split("|")[0].strip(),
      )
    if self.year:
      self._parseYearEndPage(soup)
    elif soup.select("table"):
      self._parseOldStylePage(soup)
    else:
      self._parseNewStylePage(soup)
        
  def fetchEntries(self):
      """차트에서 해당 차트 데이터를 가져오고, BeautifulSoup을 사용하여 데이터를 파싱합니다"""
      if not self.date:
        if not self.year:
          # fetch latest chart
          url = f"{_TARGET_SITE}/charts/{self.name}"
        else:
          url = f"{_TARGET_SITE}/charts/year-end/{self.year}/{self.name}"
      else:
        url = f"{_TARGET_SITE}/chart/{self.name}/{self.date}"
        
      session = _get_session_with_retries(max_retries=self._max_retries)
      req = session.get(url, timeout= self._timeout)
      if req.status_code == 404:
        message = "Chart not found (perhaps the name is misspelled?)"
        raise BillboardNotFoundException(message)
      req.raise_for_status()
      
      soup = BeautifulSoup(req.text, "html.parser")
      self._parsePage(soup)

def _get_session_with_retries(max_retries):
  session = requests.Session()
  session.mount(
    _TARGET_SITE,
    requests.adapters.HTTPAdapter(max_retries = max_retries),
  )
  return session
