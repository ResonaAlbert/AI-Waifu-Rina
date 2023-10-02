
import speech_recognition as sr

# 定义语音识别线程函数
def speech_recognition_Function(recognizer):
    # 定义关键词列表
    keywords = ["你好", "在吗", "奈奈"]
    # 定义聊天状态
    DuringChatting = True

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
                return recognized_text
        else:
            # 识别语音
            recognized_text = recognizer.recognize_google(audio, language="zh-CN")
            # 判断语音识别结果是否包含关键词
            # 判断是否包含关键词
            for keyword in keywords:
                if keyword in recognized_text:
                    print("你说的是：", recognized_text)
                    # 更新问题列表
                    return recognized_text

    # 判断是否识别到语音
    except sr.UnknownValueError:
        print("抱歉，无法识别你说的内容。")
        return ""
    # 判断请求是否错误
    except sr.RequestError as e:
        print("出现请求错误：", e)
        return ""
    