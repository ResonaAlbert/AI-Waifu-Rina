import time
from HealthInfo.InfoUpdate import JSONInfo_update
from LLM_tools.zhipuai_API import ask_zhipu

def LLM_module(question):
    Use_LLM = True
    if Use_LLM == True:
        response = ask_zhipu(question)
    else:
        response = question
    #response = '' + question
    time.sleep(0)
    last_talk_time = time.time()
    filename = 'PersonStatus.json'
    #path = "PersonStatus.json"
    JSONInfo_update(filename, "last_talk_time", last_talk_time)

    return response