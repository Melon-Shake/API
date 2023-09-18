import pandas as pd
import psycopg2
from config.db_info import db_params
import random


gpt_data = pd.read_csv("C:/Users/eagls/chatgpt1.csv")
a = gpt_data.dropna(subset=['hashtag', 'Username', 'Datetime'])

top_values = a['hashtag'].value_counts().head(100)
filtered_data = a[a['hashtag'].isin(top_values.index)]

# 중복되지 않은 처음 10,000개의 이름 가져오기
unique_names = filtered_data['Username'].drop_duplicates().head(18000).tolist()
print(unique_names)

def replace_username(row):
    if unique_names and row['Username'] not in unique_names:
        new_name = unique_names.pop(0)
        return new_name
    return row['Username']

# 'Username' 컬럼에만 적용
filtered_data['Username'] = filtered_data.apply(replace_username, axis=1)

# 중복된 이름 바꾸기
username_counts = filtered_data['Username'].value_counts()
duplicate_names = username_counts[username_counts > 1].index.tolist()

for duplicate_name in duplicate_names:
    duplicate_rows = filtered_data[filtered_data['Username'] == duplicate_name]
    if unique_names:
        new_name = unique_names.pop(0)
        filtered_data.loc[duplicate_rows.index, 'Username'] = new_name

# 남은 행도 바꾸기
filtered_data_length = len(filtered_data)
unique_names_length = len(unique_names)

if unique_names_length > 0:
    for i in range(10000, filtered_data_length):
        filtered_data.loc[i, 'Username'] = unique_names[i % unique_names_length]
else:
    print("Error: unique_names list is empty")

selected_columns = filtered_data[['Username', 'hashtag','Datetime']]

value_to_song = {'[]':'Blueming',
"['#ChatGPT']":"Meaning of you", 
"['#chatgpt']":"Friday (feat.Jang Yi-jeong)",
"['#chatGPT']":"Autumn morning",
"['#ChatGPT', '#AI']":"Hold my hand",                       
"['#ChatGPT,']":"Palette (feat. G-DRAGON)",
"['#AI', '#ChatGPT']":"eight(Prod.&Feat. SUGA of BTS)",
"['#ChatGPT.']":"Love poem",
"['#NewsPicks']":"Secret Garden",
"['#AI']":"Celebrity",   
"['#ChatGPT', '#OpenAI']":"strawberry moon",                                        
"['#ChatGPT?']":"Time & Faith",   
"['#ChatGPT:']":"Knees",
"['#meme', '#ai', '#ailaunchpad', '#cryptolaunchpad', '#chatgpt', '#chatgpt3', '#ArtificialIntelligence', '#aiprojects']":"Ah puh",
"['#OpenAI', '#ChatGPT']":"BBIBBI",
"['#note']":"Twenty-three",
"['#ArtificialIntelligence']":"Dear Name",
"['#ChatGPT', '#ChatGPT']":"above the time",
"['#Microsoft', '#ChatGPT']":"Rain Drop",
"['#AI', '#MachineLearning', '#DataScience', '#ArtificialIntelligence']":"Give You My Heart",
"['#AI', '#deeplearning']":"The shower",
"['#MidJourney', '#OpenAi', '#GPT', '#StableDiffusion2', '#DallE', '#ChatGPT', '#imagine']":"Heartless",
"['#cryptocurrencies', '#MachineLearning', '#AI', '#Python', '#DeepLearning', '#100DaysOfCode', '#fintech', '#nocode', '#bitcoin', '#cybersecurity', '#cybersecurite', '#inSurTech', '#ChatGPT']":"Good day",
"['#Chatgpt']":"Ending Scene",
"['#OpenAI']":"unlucky",
"['#Microsoft', '#OpenAI', '#ChatGPT']":"My old story",
"['#Yahooニュース']":"NAKKA (with IU)",
"['#SmartNews']":"Every End of the Day",
"['#Microsoft']":"My sea",
"['#Togetter']":"SoulMate (feat. IU)",
"['#ChatGPT', '#IA']":"Through the Night",
"['#ChatGPT', '#ArtificialIntelligence']":"Sleepless rainy night", 
"['#Chatbot']":"Winter Sleep",
"['#thread', '#ChatGPT']":"GANADARA (Feat. IU)",
"['#Google', '#ChatGPT']":"Not Spring, Love, or Cherry Blossoms",
"['#IA']":"Coin",
"['#meme', '#ai', '#ailaunchpad', '#cryptolaunchpad', '#chatgpt', '#chatgpt3', '#ArtificialIntelligence', '#aiprojects', '#AIPADmeme']":"Lullaby",
"['#ai', '#chatgpt']":"Epilogue",
"['#ChatGPT', '#Microsoft']":"LILAC", 
"['#ChatGpt']":"Troll (Feat. DEAN)",
"['#Tech', '#NewsFlash', '#Technology', '#Bot', '#News']":"Into the I-LAND",
"['#ChatGPT', '#Google']":"People Pt.2 (feat. IU)",
"['#AI', '#bigdata', '#DataScience', '#ArtificialIntelligence', '#bigdata,']":"Flu", 
"['#technology', '#technologynews', '#technews']":"Can't Love You Anymore (With OHHYUK)",
"['#CHATGPT']":"Drama",
"['#ArtificialIntelligence', '#ChatGPT']":"Nitpicking" ,
"['#chatgpt', '#ai']":"Fry’s Dream",
"['#ChatGPT', '#ChatGPTGOD', '#chatgpt3', '#gpt4', '#OpenAI', '#ChatSonic', '#searchengineoptimization']":"Love Lee",
"['#']":"I love you",
"['#ai']":"Last Goodbye",
"['#technology', '#tech', '#technews', '#teknocks']":"Time And Fallen Leaves",
'["#ChatGPT\'s"]': "HAPPENING",
"['#ChatGPT', '#AI', '#Research']":"How can I love the heartbreak, you're the one I love",
"['#ai', '#ml', '#dl']" :"How People Move",
"['#ChatGPT', '#WhatsApp']":"Endless dream, good night",
"['#WorldNews', '#Please_Share_if_you_agree']":"Blue Moon",
"['#AI', '#AIPad', '#ailaunchpad', '#cryptolaunchpad', '#crypto', '#chatgpt', '#ArtificialIntelligence', '#aiprojects']":"Way Back Home",  
"['#ai', '#ChatGPT']":"라면인건가",
"['#ChatGPT', '#OpenAIChatGPT']":"DINOSAUR",
"['#Microsoft', '#OpenAI,', '#ChatGPT']":"Reality",
"['#chatGPT.']":"Melted",
"['#FETC']":"Officially missing you" ,
"['#IA', '#ChatGPT']":"200%",
"['#chatgtp']":"Endless",                         
"['#technology', '#innovation', '#chatGPT', '#openai', '#programming']":"bad days",  
"['#ChatGPT', '#ai']":"Moonlight",             
"['#Thread', '#ChatGPT']":"Happening Again",    
"['#roboticsainews', '#ai', '#artificialintelligence', '#digitaltransformation', '#technology', '#futurework', '#engineering', '#automation']":"You Proof",  
"['#ChatGPT!']":"You Get Me So High",  
"['#SmartCity', '#digital', '#digitalhealth', '#health']":"You Shook Me All Night Long",   
"['#Technology']":"You Give Love A Bad Name",         
"['#chatGPT', '#AI']":"You Need To Calm Down",                                  
"['#robot', '#robotics']":"Young And Beautiful",                                        
"['#TekeTekBilim']":"How Do You Think",                                          
"['#ArtificialIntelligence', '#education']":"좋아좋아" ,                       
"['#节点', '#梯子', '#小火箭加速器', '#翻墙软件', '#科学上网', '#翻墙VPN', '#梯子推荐', '#翻墙加速器', '#推特账号', '#脸书账号', '#飞机账号', '#YouTube号', '#谷歌邮箱', '#tiktok号', '#苹果id', '#ins号']":"여권 (with 박재정)",
"['#プレジデントオンライン']":"일종의 고백 One Confess",                                  
"['#thread', '#chatgpt']":"DEJAVU (Feat. Jay Park) (Prod. by Slom)",  
"['#ChatGPT', '#artificalintelligence']":"Passionate Goodbye (Vocal Lee Ji Hyung)",            
"['#chatgpt', '#openai']":"HUG (Feat. Zion.T, Wonstein) (Prod. by Slom)", 
"['#quantumcomputing,', '#ChatGPT']":"NOT SORRY (Feat. pH-1) (Prod. by Slom)",                               
"['#ChatGPT', '#twlz']":"Me You (feat. Baek Yerin)",                                                  
"['#Bitcoin']":"잘가요, 괜찮아요",                                                           
"['#AI', '#chatGPT']":"Crazy Excuse",                                                
"['#Microsoft', '#ChatGPT', '#OpenAI']":"GO HIGH (Prod. by CODE KUNST)",                                             
"['#ChatGPT', '#OpenAI', '#Microsoft']":"내 입술 따뜻한 커피처럼",                                   
"['#1']":"퇴근버스",                                                                 
"['#123INFO']":"돌아가자 Go Back",                                                                  
"['#Google']":"Again (Prod.V.O.S)",                                                                 
"['#ai', '#aitools', '#chatgpt', '#youtubeautomation', '#startups']":"Anemone",               
"['#tech']":"So you",                              
"['#черномырдин', '#chatgpt', '#artificialAI']":"바람아 멈추어다오",              
"['#Entrepreneur', '#ChatGPT', '#Ready2Start']":"지우는 노래",   
"['#openai', '#ChatGPT']":"와",                                         
"['#OpenAI', '#Google']":"그 사람 많이 사랑했나요",                                
"['#M3tatranca', '#NFT', '#nftart', '#chatGPT']":"New Future",                                   
"['#KI', '#ChatGPT']":"I Am Lee Young Ji",                                           
"['#スマートニュース']":"반",                                          
"['#ChatGPT', '#chatgpt3']":"너 - Bonus Track/Techno Version",                                  
"['#AI', '#DataScience', '#ArtificialIntelligence', '#bigdata']":"바꿔"}
selected_columns['hashtag'] = selected_columns['hashtag'].map(value_to_song)

conn = psycopg2.connect(**db_params)
cursor = conn.cursor()
#회원가입 사용자 생성
for _, row in filtered_data.iterrows():
  
   
    # 여기에서는 index 대신 _ (언더스코어)를 사용하여 무시합니다.
    password = row['Username']  # Username을 password로 사용

    # 랜덤하게 남자 또는 여자 선택
    gender = random.choice(['M', 'F'])

    # 18세에서 65세 사이의 랜덤한 나이 생성
    age = random.randint(16, 85)

    email = row['Username'] + '@play.com'
    insert_query = f'INSERT INTO \"user\"(password,email,name) values (%s, %s,%s) RETURNING id;'
    insert_query1 = f'INSERT INTO user_properties(gender,age,user_id) values (%s,%s,%s);'

    # 중복 확인을 위해 SELECT 쿼리 실행
    select_query = f'SELECT id FROM "user" WHERE email = %s;'
    cursor.execute(select_query, (email,))

    existing_record = cursor.fetchone()

    # 중복 레코드가 없을 때만 INSERT 실행
    if existing_record is None:
        try:
            cursor.execute(insert_query, (password, email, row['Username']))
            user_query_id = cursor.fetchone()[0]
            cursor.execute(insert_query1, (gender, age, user_query_id))
            conn.commit()  # 커밋
        except psycopg2.Error as e:
            print("에러 발생:", e)
            conn.rollback()  # 롤백
    else:
        print(f"중복 레코드 발견: {email}")

#사용자 행동데이터 생성
for index, row in selected_columns.iterrows():
    cursor.execute("SELECT name FROM spotify_tracks;")
    all_songs = cursor.fetchall()

    hashtag = row['hashtag']
    if hashtag == '[]':
        hashtag = random.choice(all_songs)[0]
    else:
        hashtag = value_to_song.get(hashtag, hashtag)
    
    email = row['Username'] + '@play.com'
    user_query = "SELECT id FROM \"user\" WHERE email = %s;"
    user_values = (email,)
    cursor.execute(user_query, user_values)
    user_query_result = cursor.fetchone()
    if user_query_result:
        user_id = user_query_result[0]
    else:
        user_id = None
    
    track_title = row['hashtag']
    track_search = "SELECT id from spotify_tracks where name = %s"
    track_value = (track_title,)
    cursor.execute(track_search, track_value)
    track_query_result = cursor.fetchone()
    if track_query_result is not None:
        track_id = track_query_result[0]
        # 나머지 코드 작성
    else:
        # track_query_result가 None인 경우의 처리
        print("No track data found.")
    
    datetime = row['Datetime']
    search_query = "INSERT INTO search_log_tracks(created_datetime,spotify_tracks_id,user_id) values (%s,%s,%s);"
    user_values = (datetime,track_id, user_id)
    cursor.execute(search_query, user_values)
    conn.commit()  # 커밋