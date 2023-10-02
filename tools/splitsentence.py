import jieba
import re

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
        if len(sentence) < min_length:
            # 获取下一个句子
            next_sentence = sentences[i + 1]
            # 合并两个句子
            sentences[i] = sentence + next_sentence
            # 删除下一个句子
            sentences.pop(i + 1)

    return sentences


""" # 要分割的日语文本
japanese_text = "こんにちは。元気ですか？お元気ですか？さようなら。"

# 调用函数进行句子分割
sentences = split_japanese_sentences(japanese_text)

# 打印分割后的句子
for sentence in sentences:
    print(sentence)

# 调用函数并传入要分割的汉语文本
input_text = "你好，我是一个自然语言处理示例。我正在测试分割汉语文本的功能。希望这个示例对你有帮助！"
sentences = split_chinese_text(input_text)

# 打印分割后的短句
for sentence in sentences:
    print(sentence) """
