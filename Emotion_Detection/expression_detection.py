from cemotion import Cemotion
from HealthInfo import InfoUpdate as IU

def expression_detection_module(response):        
    c = Cemotion()
    Sentiments = c.predict(response)  
    # Sentiments = SECheck.infer(response)
    print("情感等级: ", Sentiments)

    if Sentiments >= 0.9: 
        if IU.JSONInfo_get('./PersonStatus.json', "heartrate") > 90:
            hotkey = 6
        else:
            hotkey = 19
    elif Sentiments >= 0.7:
        hotkey = 9
    elif Sentiments >= 0.3:
        hotkey = 1
    else:
        hotkey = 8

    return hotkey, Sentiments