import speech_recognition as sr

# 初始化Recognizer对象
recognizer = sr.Recognizer()

# 使用默认麦克风作为音频源
microphone = sr.Microphone()

with microphone as source:
    print("请说话...")
    recognizer.adjust_for_ambient_noise(source)  # 自动适应环境噪音
    audio = recognizer.listen(source)  # 监听麦克风输入

print("识别中...")

# 使用recognize_sphinx进行语音识别
try:
    text = recognizer.recognize_sphinx(audio, language="zh-CN")
    print("识别结果：", text)
except sr.UnknownValueError:
    print("无法识别音频")
except sr.RequestError as e:
    print("请求错误：", e)
