import os
import speech_recognition as sr
import threading
import time
import json
from flask import Flask, request, jsonify
import asyncio
########
from HealthInfo.InfoUpdate import JSONInfo_update, JSONInfo_get
from VITS_tools.voice_vits import VITS_module, play_all_audio
from tools.QuestionStatusUpdate import use_questionlist, update_questionlist
from LLM_tools import AskLLM
from SentimentEngine.SentimentEngine import SentimentEngine
from VTS_tools.VTS_Module import VTS_threading
from cemotion import Cemotion
import demand
from expression_detection import expression_detection_module
from speech_recognition_module import speech_recognition_Function
#from LLM_tools.LLM.LLM_module import LLM_module
#import winsound
#import random
#import string
#from requests_toolbelt.multipart.encoder import MultipartEncoder
#import requests

# Setting Function
SpeechInput_Function = False
ClientInput_Function = False
KeyboardInput_Function = True
VITS_Funtion = True
VTS_Function = True
#不分割文本课程
VITS_once = False
SentimentEngineFunction = True

#### recording and speech recognize ####
# 创建一个Recognizer对象
recognizer = sr.Recognizer()



# 定义语音识别线程函数
def speech_recognition_thread():
    # 定义全局变量
    global question_list
    
    while True:
        if Question != "":
            Question = speech_recognition_Function(recognizer)
            update_questionlist(question_list, Question)

# 定义一个函数inputfromkeyboard，用于从键盘输入内容
def keyboard_thread():
    # 定义一个全局变量question_list
    global question_list
    # 循环，直到输入为空
    while True:
        # 定义一个变量Question，用于存储输入的内容
        Question = input('请输入内容：\n')
        # 如果输入的内容为空，则打印no input
        if Question == None:
            print("no input\n")
        # 否则，调用update_questionlist函数，将输入的内容添加到question_list中
        else:
            question_list = update_questionlist(question_list, Question)
        # 打印收到的内容
        print('收到问题:', Question)

# 定义flask_thread函数，用于启动flask服务
app = Flask(__name__)
def flask_thread():
    app.run(host='0.0.0.0', port=56789)

# 定义/receive_text路由，使用POST方法，用于接收文本
@app.route('/receive_text', methods=['POST'])
def receive_text():
    # 定义全局变量question_list
    global question_list
    # 获取请求中的json数据
    data = request.get_json()
    # 从json数据中获取文本
    received_text = data.get('text')
    # 打印获取的文本
    print( "Get Question：", received_text)

    # 调用update_questionlist函数，更新question_list
    question_list = update_questionlist(question_list, received_text)
    # 定义返回信息
    reply = {"message": "Question received successfully"}
    # 将返回信息转换为json格式
    reply_json = json.dumps(reply)
    # 返回json格式的信息
    return reply_json


###### main function #######
if __name__ == "__main__":

    # SentimentEngine
    if SentimentEngineFunction == True:
        dirname, filename = os.path.split(os.path.realpath(__file__))
        #print(dirname)
        path = dirname + '\SentimentEngine\paimon_sentiment.onnx'
        SECheck = SentimentEngine(path)

    #initial information
    global question_list
    #first_question = 'みなさん、こんにちは。私はバードです。アメリカから来ました。'
    first_question = '你好，我最爱的人!'
    question_list = [[True,first_question],[False,'']]
    #question_list = [[False,'],[False,'']]

    #speech part
    speech_thread = threading.Thread(target=speech_recognition_thread)
    speech_thread.daemon = True
    #Client part
    flask_server_thread = threading.Thread(target=flask_thread)
    flask_server_thread.daemon = True
    #inputfromkeyboard part
    keyboardinput_thread = threading.Thread(target=keyboard_thread)
    keyboardinput_thread.daemon = True
    #inputfromkeyboard part
    playaudio_thread = threading.Thread(target=play_all_audio)
    playaudio_thread.daemon = True
    
    #如果SpeechInput_Function为True，则启动语音输入线程
    if SpeechInput_Function == True:
        speech_thread.start()
    #如果ClientInput_Function为True，则启动客户端输入线程
    if ClientInput_Function == True:
        flask_server_thread.start()
    #如果KeyboardInput_Function为True，则启动键盘输入线程
    if KeyboardInput_Function == True:
        keyboardinput_thread.start()  
    #如果VITS_Funtion为True，则启动键盘输入线程
    if VITS_Funtion == True:
        playaudio_thread.start()
                    
    while True:
        
        #question_list [2,2]:
        #status = True/False, content = ""
        if question_list[0][0] == True:

            #from questionlist check question
            [exit_question ,question_current] = use_questionlist(question_list)
            
            task_number = demand.command_mode(question_current)
            if task_number != False:
                demand.run_task_list(task_number)
            else:
                #ask GPT for resqonse
                response = AskLLM.LLM_module(question_current)

                if SentimentEngineFunction == True:
                    hotkey, Sentiments = expression_detection_module(response)                

                if VTS_Function == True:
                    asyncio_VTS_thread = threading.Thread(target=lambda: asyncio.run(VTS_threading(hotkey)))
                    asyncio_VTS_thread.start()

                #show the Q&A
                print("Q：", question_current)
                print("A：", response)

                # VITS voice generation and play
                if VITS_Funtion == True:
                    VITS_module(response, VITS_once, "ja")
                
                if VTS_Function == True:
                    motion_hotkey = 1
                    if hotkey != motion_hotkey:
                        time.sleep(3)
                        asyncio_VTS_thread = threading.Thread(target=lambda: asyncio.run(VTS_threading(hotkey)))
                        asyncio_VTS_thread.start()

        time.sleep(0)
