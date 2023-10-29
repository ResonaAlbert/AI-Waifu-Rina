from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import winsound
import requests
import random
import string
from tools import language_tool as LT
import threading
import time
import re
import asyncio

                    
                     # 736 36 118 诗歌剧
def voice_vits(text, id=0, format="wav", lang="auto", length=1.05, noise=0.667, noisew=0.8, max=5,  sdp_ratio=0.2, filename = "out"):
    fields = {
        "text": text,
        "id": str(id),
        "format": format,
        "lang": lang,
        "length": str(length),
        "noise": str(noise),
        "noisew": str(noisew),
        "max": str(max),
        "sdp_ratio": str(sdp_ratio)
    }
    boundary = '----VoiceConversionFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    
    print("VITS start generate:")
    
    #base = "https://artrajz-vits-simple-api.hf.space"
    base = "https://guke-vits-simple-api.hf.space"
    #base = "http://127.0.0.1:23456"
    
    m = MultipartEncoder(fields=fields, boundary=boundary)
    headers = {"Content-Type": m.content_type}
    url = f"{base}/voice/bert-vits2"

    res = requests.get(url=url)
    abs_path = os.path.dirname(__file__)
    path = f"{abs_path}/audio_log/{filename}.wav"

    print("VITS generate:", '|', filename,  '|', text)

    res = requests.post(url=url, data=m, headers=headers)
    with open(path, "wb") as f:
        f.write(res.content)
    return path

def play_audio_file(folder_path, audio_file):
        audio_path = os.path.join(folder_path, audio_file)
        print("reading:", audio_file)
        winsound.PlaySound(audio_path, winsound.SND_FILENAME)

async def play_all_audio(sentences_number):
    wav_path = "./VITS_tools/audio_log"
    i = 1
    while True:
        if i > sentences_number:
            break
        filename = "out" + str(i) + ".wav"
        if os.path.exists(os.path.join(wav_path, filename)):
            print("playing:", filename)
            audio_path = os.path.join(wav_path, filename)
            winsound.PlaySound(audio_path, winsound.SND_FILENAME)
            #play_audio_file(wav_path, filename)
            i = i + 1
    print("check audio end!")

    # 获取文件夹内的所有文件列表
    file_list = os.listdir(wav_path)
    # 逐个删除文件
    for file in file_list:
        os.remove(os.path.join(wav_path, file))
    print("delete audio end!")

async def voice_vits_seperate(text, LANGUAGE):
        i = 1
        for sentence in text:
            filename = "out" + str(i)
            voice_vits(text=sentence, lang=LANGUAGE, filename = filename)
            i += 1

async def VITS_module(response, VITS_once = False, LANGUAGE = "ja" ):
    LANGUAGE = "ja" # LANGUAGE = ja en ko zh
    #LANGUAGE = "zh"
    response_JP = LT.translate_to_japanese(response)
    # replace text content
    response_JP = response_JP.replace("兄弟", "お兄ちゃん")
    response_JP = LT.convert_kanji_to_hiragana(response_JP)

    if VITS_once == False:
        response_JP_sentences = LT.split_japanese_sentences(response_JP)
    else:
        response_JP_sentences = [response_JP]
    for i in range(len(response_JP_sentences)):
         if response_JP_sentences[i] == '':
            del response_JP_sentences[i]

    #print(response_JP_sentences)
    VITS_thread = threading.Thread(target=lambda: asyncio.run(voice_vits_seperate(response_JP_sentences, LANGUAGE)))
    VITS_thread.start()
    playaudio_thread = threading.Thread(target=lambda: asyncio.run(play_all_audio(len(response_JP_sentences))))
    playaudio_thread.start()
    
    playaudio_thread.join()


