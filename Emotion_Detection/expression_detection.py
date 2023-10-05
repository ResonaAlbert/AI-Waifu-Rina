from cemotion import Cemotion
from HealthInfo import InfoUpdate as IU

def expression_detection_module_AI(response):        
    c = Cemotion()
    Sentiments = c.predict(response)  
    # Sentiments = SECheck.infer(response)
    print("情感等级: ", Sentiments)

    if Sentiments >= 0.9: 
        if IU.JSONInfo_get('./PersonStatus.json', "heartrate") > 90:
            emotion = 'love'
        else:
            emotion = 'happy'
    elif Sentiments >= 0.7:
        emotion = 'normal'
    elif Sentiments >= 0.3:
        emotion = 'cool'
    else:
        emotion = 'hate'

    return emotion, Sentiments

def expression_detection_module_USER(Question, audio):        
    c = Cemotion()
    Sentiments = c.predict(Question)  
    # Sentiments = SECheck.infer(response)
    print("情感等级: ", Sentiments)

    # sleep quality, heart rate, clock
    # text, audio emotion
    # face emotion
    heartrate = IU.JSONInfo_get('./PersonStatus.json', "heartrate")

    if Sentiments >= 0.9:
        USER_emotion_status = 'good'
    else:
        USER_emotion_status = 'normal'

    return USER_emotion_status, Sentiments
