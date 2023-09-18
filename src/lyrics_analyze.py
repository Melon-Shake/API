import pandas as pd
import psycopg2
from config.db_info import db_params


def lyrics_analyze():
    words_dict = {
    "romantic_words" : ["행복","happ","춤","dance","사랑","Lov","설레임","Flutter","눈빛","Gaze","향기","Fragrance","미소","Smile","고요한","Calm","마음","Heart","떨림","Tremor","감동","Emotion","애정","Affection","데이트","Date","포옹","Hug","달콤한","Sweet","서정적인","Poetic","미소짓다","Smile","아름다운","Beautiful","애틋한","Tender","영원한","Eternal","좋아","like","아싸"],
    "adventurous_words" : ["힘들","성장","grow","여행","Travel","모험","Adventure","자유","Freedom","신비로운","Mysterious","평화","Peace","여유","Leisure","풍경","Scenery","천천히","Slowly","넓은","Vast","감각","Sensation","모험가","Adventurer","원하는","Admire","자유로운","Free","휴식","Rest","흐르는","flowing""세계","world","새로운","new""꿈","Dream","자연","Nature","순간","moment","지금","now"],
    "powerful_words" : ["춤","dance","열정","Passion","강렬한","Intense","에너지","Energy","불타는","Burning","도전","Challenge","화려한","Glamorous","승리","Victory","동기","Motiv","끝없는","Endless","전진","Advance","도전적인","Challenging","승부욕","Competitiveness","자신감","Confidence","극적","Dramat","화끈한","Fiery","열정","passion","열렬한","Fervent","의지","Determination","목표","Goal","힘","power"],
    "depressed_words" : ["이별","farewell","놓치","lose","아픔","아프","pain","후회","regreat","울적한","Melancholic","회상","Recollection","눈물","Tear","고요","Quiet","그리움","Longing","허전함","Emptiness","단념","Resignation","쓸쓸한","Solitary","깊은","Deep","서글픈","Sorrowful","고독한","Lonely","추억","Memory","뒤","back","아련하","faint","심상찮은","Unsettling","멈추다","Pause","생각","thought","끝없","Endless","절망","Despair"]
    }

    def count_words_in_lyrics(lyrics, words_list):
        lyrics_lower = lyrics.lower()
        word_counts = {category: 0 for category in words_list}

        for category, words in words_list.items():
            for word in words:
                word_lower = word.lower()
                count = lyrics_lower.count(word_lower)
                word_counts[category] += count

        return word_counts

    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # 쿼리 작성: romantic_words와 powerful_words가 모두 0인 행을 선택
    query = "SELECT * FROM lyrics WHERE romantic_words IS NULL AND powerful_words IS NULL AND adventurous_words IS NULL AND depressed_words IS NULL;"
    dataframe = pd.read_sql_query(query, conn)


    for i, k in enumerate(zip(dataframe['content'], dataframe['id'])):
        result = count_words_in_lyrics(k[0],words_dict)
        for j in result:
            dataframe.loc[i, j] = result[j]

        track_id = dataframe.loc[i]['id']
        romantic_words = dataframe.loc[i]['romantic_words']
        adventurous_words = dataframe.loc[i]['adventurous_words']
        powerful_words = dataframe.loc[i]['powerful_words']
        depresed_words = dataframe.loc[i]['depressed_words']
        print(track_id,romantic_words,adventurous_words,powerful_words,depresed_words)
        query = f"""UPDATE lyrics
                SET romantic_words = {romantic_words}, adventurous_words = {adventurous_words}, powerful_words = {powerful_words}, depressed_words = {depresed_words}
                WHERE id = '{track_id}';"""
        cursor.execute(query)
    conn.commit()
    conn.close()