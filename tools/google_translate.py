from googletrans import Translator, LANGUAGES

def translate_to_japanese(text):
    try:
        # 创建翻译器对象
        translator = Translator()

        # 使用谷歌翻译将文本从输入语言翻译成日语
        translated = translator.translate(text, src='auto', dest='ja')

        # 返回翻译后的文本
        return translated.text
    except Exception as e:
        return str(e)

""" # 调用函数并传入要翻译的文本
input_text = "Hello, how are you?"
translated_text = translate_to_japanese(input_text)

# 打印翻译结果
print("翻译结果：", translated_text)
 """