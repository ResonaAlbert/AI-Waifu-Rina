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
                    
                     # 736 36
def voice_vits(text, id=118, format="wav", lang="auto", length=1.1, noise=0.667, noisew=0.8, max=5, filename = "out"):
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
    
    base = "https://artrajz-vits-simple-api.hf.space"
    #base = "http://127.0.0.1:23456"
    
    m = MultipartEncoder(fields=fields, boundary=boundary)
    headers = {"Content-Type": m.content_type}
    url = f"{base}/voice"

    res = requests.post(url=url, data=m, headers=headers)
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
        winsound.PlaySound(audio_path, winsound.SND_FILENAME)
        os.remove(os.path.join(folder_path, audio_file))

    # 获取子文件夹中的所有文件
    #files = os.listdir(folder_path)
    # 逐个删除这些文件
    #for file in audio_files:
    #    os.remove(os.path.join(folder_path, file))

async def play_all_audio():
    start_time = time.time()
    wav_path = "./VITS_tools/audio_log"
    while True:
        if LT.check_dir_empty(wav_path) == False:
            start_time = time.time()
            play_audio_files(wav_path)
        if time.time() - start_time > 20:
            break
            # time.sleep(0.5)
    print("check audio end!")

def voice_vits_seperate(text, LANGUAGE):
        i = 1
        for sentence in text:
            filename = "out" + str(i)
            voice_vits(text=sentence, lang=LANGUAGE, filename = filename)
            i += 1
        return None

async def VITS_module(response, VITS_once, LANGUAGE):
    LANGUAGE = "ja" # LANGUAGE = ja en ko zh
    #LANGUAGE = "zh"
    response_JP = LT.translate_to_japanese(response)
    response_JP = response_JP.replace("兄弟", "お兄ちゃん")
    if VITS_once == False:
        response_JP_sentences = LT.split_japanese_sentences(response_JP)
        VITS_thread = threading.Thread(target=voice_vits_seperate(response_JP_sentences, LANGUAGE))
        VITS_thread.start()
    else:
        #filename = "out"
        voice_vits(text=response_JP, lang=LANGUAGE, filename = "out")
