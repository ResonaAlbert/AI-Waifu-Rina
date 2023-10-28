import time
from HealthInfo import InfoUpdate
from LLM_tools import zhipuai_API
from LLM_tools import ALI

def LLM_module(question):
    Use_LLM = True
    if Use_LLM == True:
        #response = zhipuai_API.ask_zhipu(question)
        #response = zhipuai_API.ask_character(question)
        response = ALI.QWEN(question)
        #response = 'はるのこうえんは、わたしにとって、とてもおもいでふかいばしょです。これからも、はるになると、こうえんにさんぽにいき、はるのかぜをかんじながら、ゆっくりとすごしたいとおもっています。'
    else:
        response = question
    #response = '' + question
    time.sleep(0)
    last_talk_time = time.time()
    filename = 'PersonStatus.json'
    #path = "PersonStatus.json"
    InfoUpdate.JSONInfo_update(filename, "last_talk_time", last_talk_time)

    return response