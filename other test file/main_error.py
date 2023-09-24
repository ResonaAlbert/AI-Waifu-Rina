import speech_recognition as sr
import threading
import time
from flask import Flask, request

app = Flask(__name__)
recognized_text = ""
listening = False

# 创建一个Recognizer对象
recognizer = sr.Recognizer()

def is_speaking(volume_threshold=50):
    global listening
    with sr.Microphone() as source:
        print("检测中...")
        while not listening:
            audio = recognizer.listen(source)
            volume = recognizer.energy_threshold
            if volume > volume_threshold:
                print("检测到声音！")
                listening = True

def speech_recognition_thread():
    global recognized_text, listening
    while True:
        if listening:
            with sr.Microphone() as source:
                print("请说话：")
                audio = recognizer.listen(source)
                
                listening = False
                print("stop recording")

            try:
                text = recognizer.recognize_google(audio, language="zh-CN")
                print("你说的是：", text)
                recognized_text = text
            except sr.UnknownValueError:
                print("抱歉，无法识别你说的内容。")
            except sr.RequestError as e:
                print("出现请求错误：", e)

def flask_thread():
    app.run(host='0.0.0.0', port=5000)

@app.route('/receive_text', methods=['POST'])
def receive_text():
    global recognized_text
    text = request.form.get('text')
    recognized_text = text
    return "文本已接收：" + text

if __name__ == "__main__":
    speech_thread = threading.Thread(target=speech_recognition_thread)
    flask_server_thread = threading.Thread(target=flask_thread)
    sound_detection_thread = threading.Thread(target=is_speaking)
    
    speech_thread.daemon = True
    flask_server_thread.daemon = True
    sound_detection_thread.daemon = True
    
    sound_detection_thread.start()
    flask_server_thread.start()
    
    while True:
        #print("识别到的文本：", recognized_text)
        time.sleep(1)
