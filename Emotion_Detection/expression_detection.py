from cemotion import Cemotion
from HealthInfo import InfoUpdate as IU

def expression_detection_module_AI(response, user_emotion, AI_daily_emotion):
    # happy / fear / anger / disgust / normal / love / sad      
    c = Cemotion()
    Sentiments = c.predict(response)  
    # Sentiments = SECheck.infer(response)
    print("情感等级: ", Sentiments)
    if user_emotion == 'normal':
        if Sentiments >= 0.9: 
            emotion = 'happy'
        elif Sentiments >= 0.7:
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

    return emotion, Sentiments

def expression_detection_module_USER(Question, audio):        
# happy / sad / anger / disgust / normal / tired / love 


    # sleep quality, heart rate, clock

    # text
    c = Cemotion()
    text_emotion = c.predict(Question)  
    # Sentiments = SECheck.infer(response)
    print("情感等级: ", text_emotion)

    # audio emotion

    # face emotion
    # {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
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
        else:
            if heartrate > 95:           
                if text_emotion >= 0.9:
                    USER_emotion_status = 'love'
                else:
                    USER_emotion_status = 'anger'
            else:
                if text_emotion >= 0.9:
                    USER_emotion_status = 'happy'
                else:
                    USER_emotion_status = 'normal'   
    else:
        if heartrate > 95:           
            if text_emotion >= 0.9:
                USER_emotion_status = 'love'
            else:
                USER_emotion_status = 'anger'
        else:
            if text_emotion >= 0.9:
                USER_emotion_status = 'happy'
            else:
                USER_emotion_status = 'normal'            

    return USER_emotion_status, text_emotion
