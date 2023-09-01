<hr><div align="center" display="flex">
<img alt="image" src="https://user-images.githubusercontent.com/79441624/263522796-42397a69-1a33-49bf-bf3c-83c9e5e852c3.png">
</div>
<br>
## :melon: MelonShake

> **엔코아 플레이데이터 24기 팀 MelonShake** <br/> **개발기간: 2023.08 ~ 2023.09**

<br>

__음원정보 종합 서비스 “Melon Shake”는 주요 국내 스트리밍 사이트인 Melon에서 네이밍을 채용하며 다양한 음악 플랫폼의 기능과 데이터를 하나의 플랫폼으로 통합해 음악 검색, 음악 추천, 성향 분석 등의 기능을 제공하는 서비스입니다__


### 주요기능
```bash
국내외 음원서비스 사이트 국내통합차트
음원정보 기반 통합검색
고객 정보 기반 성향 분석 및 추천
```
---
## Architecture
![전체 아키텍처 및 기술스택](https://user-images.githubusercontent.com/51077803/264909346-a79aede1-2fad-4471-801a-7a26ff463e84.png)

**[아키텍처 대한 상세 설명은 해당 링크 참조 [#48] ](https://github.com/Melon-Shake/main_melonshake/issues/48)**

---
### 디렉토리 구조
#### API
```bash
.
├── Pipfile
├── TotalApi.py
├── getTokenByRefreshToken.py
├── inputAlbumDataToDB.py
├── inputArtistDataToDB.py
├── inputTrackDataToDB.py
├── lib
│   └── module.py
├── lyric.py
├── model
│   ├── database.py
│   ├── spotify_client.py
│   └── spotify_token.py
├── sp_track.py
├── test_getSearchResult.py
└── update_token.py
```
#### FRONT
```bash
├── HELP.md
├── README.md
├── build
│   ├── libs
│   │   └── melon_shake_webapp-0.1.0.jar
│   ├── resolvedMainClassName
│   └── tmp
│   ├── bootJar
│   │   └── MANIFEST.MF
│   └── compileJava
│   └── previous-compilation-data.bin
├── build.gradle
├── gradle
│   └── wrapper
│   ├── gradle-wrapper.jar
│   └── gradle-wrapper.properties
├── gradlew
├── gradlew.bat
├── settings.gradle
└── src
├── main
│   ├── java
│   │   └── com
│   │   └── example
│   │   └── melon_shake_webapp
│   │   ├── MelonShakeWebappApplication.java
│   │   ├── controller
│   │   │   ├── HomeController.java
│   │   │   ├── RegisterController.java
│   │   │   └── SearchController.java
│   │   └── data
│   │   ├── LoginData.java
│   │   ├── RegistrationData.java
│   │   ├── SearchData.java
│   │   ├── SearchDataEmail.java
│   │   └── TrackRankingData.java
│   └── resources
│   ├── application.properties
│   └── static
│   ├── HatchfulExport-All.zip
│   ├── css
│   ├── home.html
│   ├── js
│   ├── register.html
│   └── search.html
└── test
```
---

## 🐈 Stacks (TBC)
### Environment
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=Visual%20Studio%20Code&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white)
![Github](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white)
![intellijidea](https://img.shields.io/badge/intellijidea-e8e8e7?style=for-the-badge&logo=intellijidea&logoColor=000000)
![Linux](https://img.shields.io/badge/linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![amazonec2](https://img.shields.io/badge/amazonec2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white)

### API
![fastapi](https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white)

### RDBMS
![postgresql](https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![amazonrds](https://img.shields.io/badge/amazonrds-527FFF?style=for-the-badge&logo=amazonrds&logoColor=white)

### Development
![python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![bootstrap](https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Springboot](https://img.shields.io/badge/Springboot-6DB33F?style=for-the-badge&logo=Springboot&logoColor=white)
![thymeleaf](https://img.shields.io/badge/thymeleaf-005F0F?style=for-the-badge&logo=thymeleaf&logoColor=white)
![airflow](https://img.shields.io/badge/apache_airflow-white?style=for-the-badge&logo=apacheairflow&logoColor=017CEE)
<!-- ![jenkins](https://img.shields.io/badge/apache_jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white) -->
<!-- ![spark](https://img.shields.io/badge/Spark-F05032?style=for-the-badge&logo=apacheSpark&logoColor=white) -->
![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)

---
### Repository
  - **API** : [MelonShake API](https://github.com/Melon-Shake/API)
 - **FRONT** : [MelonShake FRONT](https://github.com/Melon-Shake/Melon-Front)
---


## 👀 주요출처

> **SPOTIFY API** : [SPOTIFY](https://developer.spotify.com/documentation/web-api)
> **GENIUS API** : [GENIUS](https://docs.genius.com/)

<!-- ## 시작 가이드
### Requirements
For building and running the application you need:

- [TBU](TBU)
- [TBU](TBU)
- [TBU](TBU)

### Installation
``` bash
TBU
```
--- -->
