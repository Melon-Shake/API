words_dict = {
"Romantic_words" : ["행복","happ","춤","dance","사랑","Lov","설레임","Flutter","눈빛","Gaze","향기","Fragrance","미소","Smile","고요한","Calm","마음","Heart","떨림","Tremor","감동","Emotion","애정","Affection","데이트","Date","포옹","Hug","달콤한","Sweet","서정적인","Poetic","미소짓다","Smile","아름다운","Beautiful","애틋한","Tender","영원한","Eternal","좋아","like","아싸"],
"Adventurous_words" : ["성장","grow","여행","Travel","모험","Adventure","자유","Freedom","신비로운","Mysterious","평화","Peace","여유","Leisure","풍경","Scenery","천천히","Slowly","넓은","Vast","감각","Sensation","모험가","Adventurer","원하는","Admire","자유로운","Free","휴식","Rest","흐르는","flowing""세계","world","새로운","new""꿈","Dream","자연","Nature","순간","moment","지금","now"],
"Powerful_words" : ["춤","dance","열정","Passion","강렬한","Intense","에너지","Energy","불타는","Burning","도전","Challenge","화려한","Glamorous","승리","Victory","동기","Motiv","끝없는","Endless","전진","Advance","도전적인","Challenging","승부욕","Competitiveness","자신감","Confidence","극적","Dramat","화끈한","Fiery","열정","passion","열렬한","Fervent","의지","Determination","목표","Goal"],
"Depresed_words" : ["이별","farewell","놓치","lose","아픔","아프","pain","후회","regreat","울적한","Melancholic","회상","Recollection","눈물","Tear","고요","Quiet","그리움","Longing","허전함","Emptiness","단념","Resignation","쓸쓸한","Solitary","깊은","Deep","서글픈","Sorrowful","고독한","Lonely","추억","Memory","뒤","back","아련하","faint","심상찮은","Unsettling","멈추다","Pause","생각","thought","끝없","Endless","절망","Despair"]
}

## 그리워하다
lyrics = """사랑을 만나 이별을 하고
수없이 많은 날을 울고 웃었다
시간이란 건 순간이란 게
아름답고도 아프구나 (yeah)

낭만 잃은 시인 거의 시체 같아
바라고 있어 막연한 보답
아픔을 피해 또 다른 아픔을 만나
옆에 있던 행복을 못 찾았을까?

너를 보내고 얼마나
나 많이 후회했는지 몰라
지금 이 순간에도 많은 걸
놓치고 있는데 말이야

시간은 또 흘러 여기까지 왔네요
지금도, 결국 추억으로 남겠죠
다시 시작하는 게 (시작하는 게) 이젠 두려운걸요
이별을 만나 아플까? 봐, oh, whoa

사랑을 만나 이별을 하고
수없이 많은 날을 울고 웃었다
시간이란 건 순간이란 게
아름답고도 아프구나

Yeah, love then pain, love then pain
Yeah, let′s learn from our mistakes
우린 실패로부터 성장해 (성장해)
사랑은 하고 싶지만 nobody wants to deal

With the pain that follows, no
I understand them though
Yeah, 이해돼, 이해돼 사랑이라는 게
매일 웃게 하던 게 이제는 매일 괴롭게 해 (괴로워)
아픈 건 없어지겠지만 상처들은 영원해
But that's why it′s called beautiful pain

시간은 슬프게 기다리질 않네요
오늘도, 결국 어제가 되겠죠
다시 시작하는 게 (시작하는 게) 너무나 힘든걸요
어김없이 끝이 날까? 봐, ooh, ooh

사랑을 만나 이별을 하고
수없이 많은 날을 울고 웃었다
시간이란 건 순간이란 게
아름답고도 아프구나

사랑이란 건 멈출 수 없다
아픔은 반복돼 (반복돼)
이렇게도 아픈데 또 찾아와
사랑은 남몰래

우린 누구나가 바보가 돼
무기력하게도, 한순간에
오래도록 기다렸다는 듯
아픈 사랑 앞에 물들어가

그대를 만나 사랑을 하고
그 어떤 순간보다 행복했었다
그대는 부디 아프지 말고
아름다웠길 바란다

사랑을 만나 이별을 하고 (oh)
수없이 많은 날을 울고 웃었다
시간이란 건 순간이란 게 (oh)
아름답고도 아프구나"""


def count_words_lyrics(lyrics, words_list):
    lyrics_lower = lyrics.lower()
    word_counts = {category: 0 for category in words_list}

    for category, words in words_list.items():
        for word in words:
            word_lower = word.lower()
            count = lyrics_lower.count(word_lower)
            word_counts[category] += count

    return word_counts

# 주어진 가사와 워드 리스트로부터 단어 등장 횟수 계산
word_counts = count_words_lyrics(lyrics, words_dict)

# 결과 출력
for category, count in word_counts.items():
    print(f"{category}: {count}번")


def count_words_in_lyrics(lyrics, words_list):
    # 소문자로 변환하여 가사와 워드 리스트의 단어들을 대소문자 구분 없이 비교
    lyrics_lower = lyrics.lower()
    word_counts = {category: {word: 0 for word in words} for category, words in words_list.items()}

    for category, words in words_list.items():
        for word in words:
            word_lower = word.lower()
            count = lyrics_lower.count(word_lower)
            word_counts[category][word] = count

    return word_counts
