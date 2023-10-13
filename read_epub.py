import time
from VITS_tools import voice_vits as VITS 
import asyncio
import threading

# 指定要打开的EPUB文件的路径
file_path = './imoto.txt'

import threading
import time
import asyncio


with open(file_path, 'r', encoding='utf-8') as file:
    file_contents = file.read()
    # 将文本内容按行分割并逐行打印
    #lines = file_contents.splitlines()
    lines = 'おはようございますおは。ようございます、おはようございます、おはようございます。おはようございますおは。ようございます、おはようございます、おはようございます'
    print(len(lines))
    #for line in lines:
    #    if line != '':
    VITS_module_thread = threading.Thread(target=lambda: asyncio.run(VITS.VITS_module(lines, False, "ja")))
    VITS_module_thread.start()
    #VITS_module_thread.join()
    #        print(line)
    time.sleep(0.1)
    #print(file_contents)
