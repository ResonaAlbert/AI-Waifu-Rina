from cemotion import Cemotion
from HealthInfo import InfoUpdate as IU
from google.cloud import language_v1

def google_sentiment(text):
    # Instantiates a client
    client = language_v1.LanguageServiceClient()

    # The text to analyze
    #text = u"Hello, world!"
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    #print("Text: {}".format(text))
    #print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

    return sentiment.score

def loveValue_Update(Sentiments):
    if Sentiments < -0.5:
        loveValue = IU.JSONInfo_get('./PersonStatus.json', "loveValue")
        loveValue_new = loveValue - 1
        IU.JSONInfo_update('./PersonStatus.json', "loveValue", loveValue_new)
        print("loveValue: ", loveValue_new)
    if Sentiments > 0.5:
        loveValue = IU.JSONInfo_get('./PersonStatus.json', "loveValue")
        loveValue_new = loveValue + 1
        IU.JSONInfo_update('./PersonStatus.json', "loveValue", loveValue_new)
        print("loveValue: ", loveValue_new)
    return None

def expression_detection_module_AI(SentimentEngineFunction, response, user_emotion):
    # happy / fear / anger / disgust / normal / love / sad      
    #c = Cemotion()
    #Sentiments = c.predict(response)  
    # Sentiments = SECheck.infer(response)
    if SentimentEngineFunction == True:
        AI_daily_emotion = IU.JSONInfo_get('./PersonStatus.json', "AI_daily_emotion")
        Sentiments = google_sentiment(response)
        print("AI Text Emotion: ", Sentiments)
        if user_emotion == 'normal':
            if Sentiments >= 0.25: 
                emotion = 'happy'
            elif Sentiments >= -0.25:
                emotion = 'normal'
            else:
                emotion = 'disgust'
        elif user_emotion == 'happy':
            emotion = 'happy'
        elif user_emotion == 'anger':
            emotion = 'fear'
        elif user_emotion == 'disgust':
            emotion = 'sad'
        elif user_emotion == 'tired':
            emotion = 'fear'
        elif user_emotion == 'love':
            emotion = 'love'
        elif user_emotion == 'sad':
            emotion = 'fear'
        else:
            emotion = 'normal'

        if AI_daily_emotion == 'negative':
            if emotion == 'happy':
                emotion = 'normal'
            if emotion == 'normal':
                emotion = 'disgust'
    else:
        emotion = "normal"

    return emotion

def expression_detection_module_USER(Question):        
# happy / sad / anger / disgust / normal / tired / love 
    # sleep quality, heart rate, clock

    # text
    #c = Cemotion()
    #text_emotion = c.predict(Question)  
    USER_text_emotion = google_sentiment(Question)
    loveValue_Update(USER_text_emotion)
    # Sentiments = SECheck.infer(response)
    # print("User TEXT Emotion: ", USER_text_emotion)

    # audio emotion

    # face emotion
    # {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    # normal happy disgust
    exit = IU.JSONInfo_get('./PersonStatus.json', "exit")
    if exit == True:
        face_emotion = IU.JSONInfo_get('./PersonStatus.json', "face_emotion")

    # heart rate
    heartrate = IU.JSONInfo_get('./PersonStatus.json', "heartrate")

    if exit == True:
        if face_emotion == 'happy':
            if heartrate > 95: 
                USER_emotion_status = 'love'
            else:
                USER_emotion_status = 'happy'
        elif face_emotion == 'Disgusted':
            USER_emotion_status = 'disgust'
        else: # normal
            if heartrate > 95:           
                if USER_text_emotion >= 0.25:
                    USER_emotion_status = 'love'
                else:
                    USER_emotion_status = 'anger'
            else:
                if USER_text_emotion >= 0.25:
                    USER_emotion_status = 'happy'
                elif USER_text_emotion >= -0.25:
                    USER_emotion_status = 'normal'
                else:
                    USER_emotion_status = 'disgust'   
    else:
        if heartrate > 95:           
            if USER_text_emotion >= 0.25:
                USER_emotion_status = 'love'
            else:
                USER_emotion_status = 'anger'
        else:
            if USER_text_emotion >= 0.25:
                USER_emotion_status = 'happy'
            elif USER_text_emotion >= -0.25:
                USER_emotion_status = 'normal'
            else:
                USER_emotion_status = 'disgust'            

    return USER_emotion_status, USER_text_emotion

def Question_Emotion_INFO(Emotionfunction = True, question_current=''):
    if Emotionfunction == True:
        USER_emotion_status, text_emotion = expression_detection_module_USER(question_current)
        # print('USER_emotion_status:', USER_emotion_status)
        # print('text_emotion:', text_emotion)
        question_current = "(" + "I am " + USER_emotion_status + " now)" + question_current
    else:
        USER_emotion_status = 'normal'
    return question_current, USER_emotion_status, 