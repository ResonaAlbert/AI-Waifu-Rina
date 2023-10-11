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
import pykakasi
import asyncio

def convert_kanji_to_hiragana(text):
    kakasi = pykakasi.kakasi()
    kakasi.setMode("J", "H")  # 将汉字转换为平假名
    kakasi.setMode("K", "H")  # 将片假名转换为平假名
    conv = kakasi.getConverter()
    result = conv.do(text)
    return result
                    
                     # 736 36 118 诗歌剧
def voice_vits(text, id=0, format="wav", lang="auto", length=1, noise=0.667, noisew=0.8, max=5, filename = "out"):
    fields = {
        "text": text,
        "id": str(id),
        "format": format,
        "lang": lang,
        "length": str(length),
        "noise": str(noise),
        "noisew": str(noisew),
        "max": str(max)
    }
    boundary = '----VoiceConversionFormBoundary' + ''.join(random.sample(string.ascii_letters + string.digits, 16))
    
    print("VITS start generate:")
    
    #base = "https://artrajz-vits-simple-api.hf.space"
    base = "https://guke-vits-simple-api.hf.space"
    #base = "http://127.0.0.1:23456"
    
    m = MultipartEncoder(fields=fields, boundary=boundary)
    headers = {"Content-Type": m.content_type}
    url = f"{base}/voice/bert-vits2?text={text}&id={id}&format=wav&length={length}"

    res = requests.get(url=url)
    abs_path = os.path.dirname(__file__)
    path = f"{abs_path}/audio_log/{filename}.wav"

    print("VITS generate:", text)
    
    with open(path, "wb") as f:
        f.write(res.content)
    #winsound.PlaySound(path, winsound.SND_FILENAME)
    
    return path

def play_audio_files(folder_path):
    # 获取指定文件夹中的所有文件
    file_list = os.listdir(folder_path)
    # 过滤出音频文件（假设扩展名是.wav）
    audio_files = [file for file in file_list if file.endswith(".wav")]
    # 按文件名排序，确保按顺序播放
    audio_files.sort()
    # 播放每个音频文件
    for audio_file in audio_files:
        audio_path = os.path.join(folder_path, audio_file)
        print("reading:", audio_file)
        winsound.PlaySound(audio_path, winsound.SND_FILENAME)
        os.remove(os.path.join(folder_path, audio_file))
        print("delete:", audio_file)

async def play_all_audio():
    global VITS_module_thread_status
    wav_path = "./VITS_tools/audio_log"
    while True:
        if VITS_module_thread_status == False:
            # last audio check
            time.sleep(1)
            if os.path.isdir(wav_path) and os.listdir(wav_path) != []: # check dir empty
                play_audio_files(wav_path)
            break
        
        if os.path.isdir(wav_path) and os.listdir(wav_path) != []: # check dir empty
            play_audio_files(wav_path)
            time.sleep(0.5)

    print("check audio end!")

async def play_all_audio0():
    start_time = time.time()
    wav_path = "./VITS_tools/audio_log"
    while True:
        if os.path.isdir(wav_path) and os.listdir(wav_path) != []: # check dir empty
            start_time = time.time()
            play_audio_files(wav_path)
        if time.time() - start_time > 20:
            break
            # time.sleep(0.5)
    print("check audio end!")

async def voice_vits_seperate(text, LANGUAGE):
        i = 1
        for sentence in text:
            filename = "out" + str(i)
            voice_vits(text=sentence, lang=LANGUAGE, filename = filename)
            i += 1
        return None

async def VITS_module0(response, VITS_once, LANGUAGE):
    LANGUAGE = "ja" # LANGUAGE = ja en ko zh
    #LANGUAGE = "zh"
    response_JP = LT.translate_to_japanese(response)
    # replace text content
    response_JP = response_JP.replace("兄弟", "お兄ちゃん")

    response_JP = convert_kanji_to_hiragana(response_JP)

    if VITS_once == False:
        response_JP_sentences = LT.split_japanese_sentences(response_JP)
        VITS_thread = threading.Thread(target=voice_vits_seperate(response_JP_sentences, LANGUAGE))
        VITS_thread.start()
    else:
        #filename = "out"
        voice_vits(text=response_JP, lang=LANGUAGE, filename = "out")

async def VITS_module(response, VITS_once, LANGUAGE):
    LANGUAGE = "ja" # LANGUAGE = ja en ko zh
    #LANGUAGE = "zh"
    response_JP = LT.translate_to_japanese(response)
    # replace text content
    response_JP = response_JP.replace("兄弟", "お兄ちゃん")

    response_JP = convert_kanji_to_hiragana(response_JP)

    if VITS_once == False:
        response_JP_sentences = LT.split_japanese_sentences(response_JP)
        VITS_thread = threading.Thread(target=lambda: asyncio.run(voice_vits_seperate(response_JP_sentences, LANGUAGE)))
        VITS_thread.start()
        global VITS_module_thread_status
        VITS_module_thread_status = True
        playaudio_thread = threading.Thread(target=lambda: asyncio.run(play_all_audio()))
        playaudio_thread.start()        
    
        if VITS_thread is not None and VITS_thread.is_alive():
            VITS_thread.join()
            VITS_module_thread_status = False

    else:
        #filename = "out"
        voice_vits(text=response_JP, lang=LANGUAGE, filename = "out")
        playaudio_thread = threading.Thread(target=lambda: asyncio.run(play_all_audio()))
        playaudio_thread.start()     
        VITS_module_thread_status = False   


