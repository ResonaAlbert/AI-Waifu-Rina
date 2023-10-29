import os
import speech_recognition as sr
import threading
import time
import json
from flask import Flask, request
import asyncio

########
from VITS_tools import voice_vits as VITS 
from tools import QuestionStatusUpdate as QSU
from tools import language_tool as LT
from VTS_tools import VTS_Module as VTS
from LLM_tools import AskLLM as LLM
from Emotion_Detection import expression_detection as EMOTION
from ASR import Speech_Recognition_Module as ASR

import demand

# Setting Function
SpeechInput_Function = False
ClientInput_Function = True
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
        Question = ASR.speech_recognition_thread(recognizer)
        if Question != "":
            QSU.update_questionlist(question_list, Question)

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
            question_list = QSU.update_questionlist(question_list, Question)
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
    question_list = QSU.update_questionlist(question_list, received_text)
    # 定义返回信息
    reply = {"message": "Question received successfully"}
    # 将返回信息转换为json格式
    reply_json = json.dumps(reply)
    # 返回json格式的信息
    return reply_json

def CHATBOT(question_current, SentimentEngineFunction):
    question_current, USER_emotion_status = EMOTION.Question_Emotion_INFO(SentimentEngineFunction, question_current)
    #ASK LLM for resqonse
    response = LLM.LLM_module(question_current)
    response = LT.remove_brackets_and_replace(response)

    #limit text
    if len(response) >100:
        response = response[:50]

    AI_emotion = EMOTION.expression_detection_module_AI(SentimentEngineFunction, response, USER_emotion_status)                
    # print('AI_emotion:', AI_emotion)    

    if VTS_Function == True:
        asyncio_VTS_thread_start = threading.Thread(target=lambda: asyncio.run(VTS.VTS_module(AI_emotion, True)))
        asyncio_VTS_thread_start.start()

    #show the Q&A
    print("Q：", question_current)
    print("A：", response)

    # VITS voice generation and play
    if VITS_Funtion == True:
        VITS_module_thread = threading.Thread(target=lambda: asyncio.run(VITS.VITS_module(response, VITS_once, "ja")))
        VITS_module_thread.start()
    # Wait for the playaudio_thread to finish
        VITS_module_thread.join()  

    if VTS_Function == True:
        asyncio_VTS_thread_end = threading.Thread(target=lambda: asyncio.run(VTS.VTS_module(AI_emotion, False)))
        asyncio_VTS_thread_end.start()

        asyncio_VTS_thread_start.join()
        asyncio_VTS_thread_end.join()


###### main function #######
if __name__ == "__main__":

    #initial information
    global question_list
    #first_question = 'みなさん、こんにちは。私はバードです。アメリカから来ました。'
    first_question = '你好' #，我最爱的人!'
    question_list = [first_question]

    #speech part
    speech_thread = threading.Thread(target=speech_recognition_thread)
    speech_thread.daemon = True
    #Client part
    flask_server_thread = threading.Thread(target=flask_thread)
    flask_server_thread.daemon = True
    #inputfromkeyboard part
    keyboardinput_thread = threading.Thread(target=keyboard_thread)
    keyboardinput_thread.daemon = True
    #如果SpeechInput_Function为True，则启动语音输入线程
    if SpeechInput_Function == True:
        speech_thread.start()
    #如果ClientInput_Function为True，则启动客户端输入线程
    if ClientInput_Function == True:
        flask_server_thread.start()
    #如果KeyboardInput_Function为True，则启动键盘输入线程
    if KeyboardInput_Function == True:
        keyboardinput_thread.start()  
                    
    while True:
        if question_list != []:
            #from questionlist check question
            question_current = QSU.use_questionlist(question_list)
            task_number, Info = demand.command_mode(question_current)
            if task_number != False:
                demand.run_task_list(task_number, Info)
            else:
                CHATBOT(question_current, SentimentEngineFunction)
