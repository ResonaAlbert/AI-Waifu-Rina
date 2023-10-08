import pykakasi

def convert_kanji_to_hiragana(text):
    kakasi = pykakasi.kakasi()
    kakasi.setMode("J", "H")  # 将汉字转换为平假名
    kakasi.setMode("K", "H")  # 将片假名转换为平假名
    conv = kakasi.getConverter()
    result = conv.do(text)
    return result

#if __name__ == "__main__":
#    japanese_text = "春は、花が咲き、空気が澄んで、とても気持ちの良い季節です。"
#    hiragana_text = convert_kanji_to_hiragana(japanese_text)
#    print(hiragana_text)
