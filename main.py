import os
import speech_recognition as sr
import threading
import time
import json
from flask import Flask, request, jsonify
########
from HealthInfo.InfoUpdate import JSONInfo_update
from VITS_tools.voice_vits import voice_vits
from tools.QuestionStatusUpdate import use_questionlist, update_questionlist
from tools.google_translate import translate_to_japanese
from tools.splitsentence import split_chinese_text, split_japanese_sentences
from LLM_tools import AskLLM
from SentimentEngine.SentimentEngine import SentimentEngine
#from LLM_tools.LLM.LLM_module import LLM_module
#import winsound
#import random
#import string
#from requests_toolbelt.multipart.encoder import MultipartEncoder
#import requests

SpeechFunction = True
FlaskFunction = False
keyboardFunction = False

VITS_funtion = False
VITS_once = False
SentimentEngineFunction = False

#### recording and speech recognize ####
# 创建一个Recognizer对象
recognizer = sr.Recognizer()

def speech_recognition_thread():
    global question_list
    # 定义关键词列表
    keywords = ["你好", "在吗", "奈奈"]
    DuringChatting = False

    while True:
        with sr.Microphone() as source:
            print("请说话：")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            print("stop recording")

        try:
            if DuringChatting == True:
                recognized_text = recognizer.recognize_google(audio, language="zh-CN")
                if recognized_text != None:
                    print("DuringChatting: ", recognized_text)
                    question_list = update_questionlist(question_list, recognized_text)
            else:
                recognized_text = recognizer.recognize_google(audio, language="zh-CN")
                # 判断语音识别结果是否包含关键词
                for keyword in keywords:
                    if keyword in recognized_text:
                        print("你说的是：", recognized_text)
                        question_list = update_questionlist(question_list, recognized_text)
                        break

        except sr.UnknownValueError:
            print("抱歉，无法识别你说的内容。")
        except sr.RequestError as e:
            print("出现请求错误：", e)

def inputfromkeyboard():
    global question_list
    while True:
        Question = input('请输入内容：')
        if Question == None:
            print("no input")
        else:
            question_list = update_questionlist(question_list, Question)
        print('收到问题:', Question)

#### text question to receive ####
app = Flask(__name__)
def flask_thread():
    app.run(host='0.0.0.0', port=56789)

@app.route('/receive_text', methods=['POST'])
def receive_text():
    global question_list
    data = request.get_json()
    received_text = data.get('text')
    print( "Get Question：", received_text)

    question_list = update_questionlist(question_list, received_text)
    reply = {"message": "Question received successfully"}
    reply_json = json.dumps(reply)
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
    first_question = 'hello world!'
    question_list = [[True,first_question],[False,'']]
    #question_list = [[False,'],[False,'']]

    #speech part
    speech_thread = threading.Thread(target=speech_recognition_thread)
    speech_thread.daemon = True
    #text part
    flask_server_thread = threading.Thread(target=flask_thread)
    flask_server_thread.daemon = True
    #text part
    keyboardinput_thread = threading.Thread(target=inputfromkeyboard)
    keyboardinput_thread.daemon = True
    
    #start input threading
    if SpeechFunction == True:
        speech_thread.start()
    if FlaskFunction == True:
        flask_server_thread.start()
    if keyboardFunction == True:
        keyboardinput_thread.start()       
    
    while True:
        
        #question_list [2,2]: fist arrow used or not, exit or nor, second arrow：question content
        #status = True/False, content = ""
        if question_list[0][0] == True:

            #from questionlist check question
            [exit_question ,question_current] = use_questionlist(question_list)
            #ask GPT for resqonse
            response = AskLLM.LLM_module(question_current)

            if SentimentEngineFunction == True:
                Sentiments = SECheck.infer(response)
                print("情感等级: ", Sentiments)

            #show the Q&A
            print("Q：", question_current)
            print("A：", response)

            # VITS voice generation and play
            if VITS_funtion == True:
                LANGUAGE = "ja" # LANGUAGE = ja en ko zh
                response_JP = translate_to_japanese(response)
                if VITS_once == True:
                    response_JP_sentences = split_japanese_sentences(response_JP)
                    for sentence in response_JP_sentences:
                        voice_vits(text=sentence, lang=LANGUAGE)
                else:
                    voice_vits(text=response_JP, lang=LANGUAGE)

        time.sleep(1)
