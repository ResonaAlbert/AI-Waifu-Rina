import threading
import asyncio
from VITS_tools.voice_vits import VITS_module

def command_mode(question):
    COMMAND = 'COMMAND'
    if question.startswith(COMMAND):
        print("enter command mode!\n")
        COMMAND_content = ':WELCOME'
        if question.find(COMMAND_content) == -1:
            print("not found command!\n")
            return False
        else:
            print("found command!\n")
            return 1 # task list　welcome
    else:
        return False
    
def run_task_list(task_number):
    if task_number == 1:
        print("task 1: COME BACK MODE\n")
        from VTS_tools.VTS_Module import VTS_threading
        
        response = "おかえりなさい、私の一番好きなお兄ちゃん！"
        VITS_once = True
        VITS_module(response, VITS_once, "ja")
            
        hotkey = 1
        asyncio_VTS_thread = threading.Thread(target=lambda: asyncio.run(VTS_threading(hotkey)))
        asyncio_VTS_thread.start()
        
        return None



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