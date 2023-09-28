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
#from LLM_tools.LLM.LLM_module import LLM_module
#import winsound
#import random
#import string
#from requests_toolbelt.multipart.encoder import MultipartEncoder
#import requests

# Setting Function
SpeechInput_Function = True
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
    # 定义关键词列表
    keywords = ["你好", "在吗", "奈奈"]
    # 定义聊天状态
    DuringChatting = True

    while True:
        # 打开麦克风
        with sr.Microphone() as source:
            print("请说话：")
            # 调整麦克风噪声
            recognizer.adjust_for_ambient_noise(source)
            # 记录语音
            audio = recognizer.listen(source)
            print("stop recording")

        try:
            # 判断聊天状态
            if DuringChatting == True:
                # 识别语音
                # google
                recognized_text = recognizer.recognize_google(audio, language="zh-CN")
                # FunASR
                #recognized_text = FunASR(audio)
                # 判断是否识别到语音
                if recognized_text != None:
                    print("DuringChatting: ", recognized_text)
                    # 更新问题列表
                    question_list = update_questionlist(question_list, recognized_text)
            else:
                # 识别语音
                recognized_text = recognizer.recognize_google(audio, language="zh-CN")
                # 判断语音识别结果是否包含关键词
                # 判断是否包含关键词
                for keyword in keywords:
                    if keyword in recognized_text:
                        print("你说的是：", recognized_text)
                        # 更新问题列表
                        question_list = update_questionlist(question_list, recognized_text)
                        break

        # 判断是否识别到语音
        except sr.UnknownValueError:
            print("抱歉，无法识别你说的内容。")
        # 判断请求是否错误
        except sr.RequestError as e:
            print("出现请求错误：", e)

# 定义一个函数inputfromkeyboard，用于从键盘输入内容
def inputfromkeyboard():
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
    keyboardinput_thread = threading.Thread(target=inputfromkeyboard)
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
            #ask GPT for resqonse
            response = AskLLM.LLM_module(question_current)

            if SentimentEngineFunction == True:
                c = Cemotion()
                Sentiments = c.predict(response)  
                # Sentiments = SECheck.infer(response)
                print("情感等级: ", Sentiments)
            
            
            if Sentiments >= 0.9: 
                if JSONInfo_get('./PersonStatus.json', "heartrate") > 90:
                    hotkey = 6
                else:
                    hotkey = 19
            elif Sentiments >= 0.7:
                hotkey = 9
            elif Sentiments >= 0.3:
                hotkey = 1
            else:
                hotkey = 8
            

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
                if hotkey != 1:
                    time.sleep(3)
                    asyncio_VTS_thread = threading.Thread(target=lambda: asyncio.run(VTS_threading(hotkey)))
                    asyncio_VTS_thread.start()

        time.sleep(0)
