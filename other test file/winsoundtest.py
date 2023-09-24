import os
import winsound
import os
import winsound
import speech_recognition as sr
import threading
import time
import json
import random
import string
from requests_toolbelt.multipart.encoder import MultipartEncoder
from flask import Flask, request, jsonify
import requests

from pydub import AudioSegment

abs_path = os.path.dirname(__file__)
need_SpeechFunction = False
base = "http://127.0.0.1:23456"

def voice_vits(text, id=0, format="wav", lang="auto", length=1, noise=0.667, noisew=0.8, max=50, sems_number=1):
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

    m = MultipartEncoder(fields=fields, boundary=boundary)
    headers = {"Content-Type": m.content_type}
    url = f"{base}/voice"
    res = requests.post(url=url, data=m, headers=headers)
    path = f"{abs_path}/audio_log/out{sems_number}.wav"

    with open(path, "wb") as f:
        f.write(res.content)
    print(path)
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

def merge_audio_files(folder_path, output_path):
    # 获取指定文件夹中的所有文件
    file_list = os.listdir(folder_path)

    # 过滤出音频文件（假设扩展名是.wav）
    audio_files = [file for file in file_list if file.endswith(".wav")]

    # 按文件名排序，确保按顺序合并
    audio_files.sort()

    # 初始化合并后的音频
    merged_audio = AudioSegment.empty()

    # 逐个合并音频文件
    for audio_file in audio_files:
        audio_path = os.path.join(folder_path, audio_file)
        audio = AudioSegment.from_file(audio_path, format="wav")
        merged_audio += audio

    # 保存合并后的音频文件
    merged_audio.export(output_path, format="wav")

LANGUAGE = "ja"
audio_txt = ['','','','','']
audio_txt[1] = 'ある日、元日本人にして公爵令嬢であるアリス-カサンドラは、'
audio_txt[2] = 'なんでも自分が下級貴族であるフランを虐めたとか。'
audio_txt[3] = 'デタラメだったが、婚約者という立場と、貴族の立場にうんざりしていたアリスはこれを受け入れる。'
audio_txt[4] = '転生したと思ったら、したくもない稽古や意味のない舞踏会ばかり。'


for i in range(1, 5):
    voice_vits(text=audio_txt[i], lang=LANGUAGE, sems_number=i)

abs_path = os.path.dirname(__file__)
print(abs_path)
#audio_path = os.path.join(abs_path, "audio_log", "out50.wav")
#winsound.PlaySound(audio_path, winsound.SND_FILENAME)

# 指定音频文件所在的文件夹路径
audio_path = os.path.join(abs_path, "audio_log")
audio_sum = os.path.join(abs_path, "audio_sum","audio.wav")

# 调用函数播放音频文件
#play_audio_files(audio_path)

# 调用函数合并音频文件
merge_audio_files(audio_path, audio_sum)
winsound.PlaySound(audio_sum, winsound.SND_FILENAME)
