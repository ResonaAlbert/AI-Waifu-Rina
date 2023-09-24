from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import winsound
from flask import Flask, request, jsonify
import requests
import random
import string

def voice_vits(text, id=726, format="wav", lang="auto", length=1.1, noise=0.667, noisew=0.8, max=50):
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
    base = "http://127.0.0.1:23456"
    m = MultipartEncoder(fields=fields, boundary=boundary)
    headers = {"Content-Type": m.content_type}
    url = f"{base}/voice"

    res = requests.post(url=url, data=m, headers=headers)
    abs_path = os.path.dirname(__file__)
    path = f"{abs_path}/audio_log/out.wav"

    with open(path, "wb") as f:
        f.write(res.content)
    #print(path)

    winsound.PlaySound(path, winsound.SND_FILENAME)
    
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

    # 获取子文件夹中的所有文件
    files = os.listdir(folder_path)
    # 逐个删除这些文件
    for file in files:
        os.remove(os.path.join(folder_path, file))