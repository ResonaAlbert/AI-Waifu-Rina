import threading
import asyncio
from VITS_tools import voice_vits as VITS 
import VTS_tools.VTS_Module as VTS
import sys

def command_mode(question):
    COMMAND = 'COMMAND'
    if question.startswith(COMMAND):
        print("enter command mode!\n")

        COMMAND_content = ':WELCOME'
        if question.find(COMMAND_content) != -1:
            print("found command!\n")
            return 1 # task list　welcome
        COMMAND_content = ':END'
        if question.find(COMMAND_content) != -1:
            print("found command!\n")
            return 2
        COMMAND_content = ':HUG'
        if question.find(COMMAND_content) != -1:
            print("found command!\n")
            return 3
        return False
    else:
        return False
    
def run_task_list(task_number):
    if task_number == 1:
        print("task 1: COME BACK MODE\n")
        
        response = "おかえりなさい、私の一番好きなお兄ちゃん！"
        VITS_once = True
        VITS_module_thread = threading.Thread(target=lambda: asyncio.run(VITS.VITS_module(response, VITS_once, "ja")))
        VITS_module_thread.start()
            
        hotkey = 19
        asyncio_VTS_thread = threading.Thread(target=lambda: asyncio.run(VTS.VTS_threading(hotkey)))
        asyncio_VTS_thread.start()
        asyncio_VTS_thread.join()
        
        return None
    if task_number == 2:
        print("task 2:END Program!\n")
        sys.exit(0)
    if task_number == 3:
        print("task 1: HUG MODE\n")
        
        response = "えへへ、お兄さんの体、あったかいです。もっとぎゅってして！"
        VITS_once = True
        VITS_module_thread = threading.Thread(target=lambda: asyncio.run(VITS.VITS_module(response, VITS_once, "ja")))
        VITS_module_thread.start()
            
        hotkey = 20
        asyncio_VTS_thread = threading.Thread(target=lambda: asyncio.run(VTS.VTS_threading(hotkey)))
        asyncio_VTS_thread.start()
        asyncio_VTS_thread.join()
    



""" print(check_start_with("Hello, world!", "Hello"))  # True
print(check_start_with("Hello, world!", "world"))  # False """

""" # 去除字符串开头的指定字符串
string = "Hello, world!"
print(string.lstrip("Hello"))  # "world!" """

""" print(check_word_in_string("Hello, world!", "Hello"))  # True
print(check_word_in_string("Hello, world!", "world"))  # True
print(check_word_in_string("Hello, world!", "goodbye"))  # False

def check_start_with(string, word):
    return string.startswith(word)

def check_word_in_string(string, word):
    index = string.find(word)
    return index
 """