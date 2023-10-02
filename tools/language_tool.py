import jieba
import re
import langid
from googletrans import Translator, LANGUAGES
import os

# 下载适用于日语的分词器数据
#nltk.download('punkt')

def split_chinese_text(text):
    # 使用jieba分词将文本分成短句
    sentences = list(jieba.cut(text, cut_all=False))

    # 将短句存储在字符串数组中
    sentence_array = []
    current_sentence = ""

    for word in sentences:
        current_sentence += word
        if word in ["。", "？", "！", "；"]:
            sentence_array.append(current_sentence)
            current_sentence = ""

    # 如果还有剩余的文本，添加到数组中
    if current_sentence:
        sentence_array.append(current_sentence)

    return sentence_array

def split_japanese_sentences(text, min_length=8):
    # 使用正则表达式定义句子分隔符（句号、问号、感叹号、省略号）
    sentence_delimiters = r'。|？|！|…'

    # 使用正则表达式分割文本为句子
    sentences = re.split(sentence_delimiters, text)

    # 去除空白句子
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    # 遍历每个句子
    for i, sentence in enumerate(sentences):
        # 如果句子长度小于指定长度，则合并到下一个句子
            if len(sentence) < min_length & i <= len(sentences):
                # 获取下一个句子
                next_sentence = sentences[i + 1]
                # 合并两个句子
                sentences[i] = sentence + next_sentence
                # 删除下一个句子
                sentences.pop(i + 1)

    return sentences

def detect_language(text):
  """
  检测输入文本的语种。

  Args:
    text: 输入文本。

  Returns:
    文本的语种，如果无法识别，返回 None。
  """

  # 使用 langid 库进行语言检测。
  result = langid.classify(text)

  # 如果无法识别，返回 None。
  if result is None:
    return None

  # 返回识别到的语言。
  return result[0]

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
    
def check_dir_empty(path):
    """
    判断指定文件夹是否为空

    Args:
        path: 指定文件夹的路径

    Returns:
        True 表示文件夹为空，False 表示文件夹不为空
    """

    if os.path.isdir(path) and os.listdir(path) == []:
        return True
    else:
        return False