import threading
import asyncio
from VITS_tools import voice_vits as VITS 
import VTS_tools.VTS_Module as VTS
import sys
import random

def command_mode(question):
    COMMAND = 'COMMAND'
    if question.startswith(COMMAND):
        print("enter command mode!\n")
        COMMAND_content = ':WELCOME'
        if question.find(COMMAND_content) != -1:
            print("found command!\n")
            Info = -1
            return 1, Info 
        COMMAND_content = ':END'
        if question.find(COMMAND_content) != -1:
            print("found command!\n")
            Info = -1
            return 2, Info
        COMMAND_content = ':HUG'
        # FORCE1, FORCE2, FORCE3
        if question.find(COMMAND_content) != -1:
            print("found command!\n")
            force = ':FORCE1'
            if question.find(force) != -1:
                #print("found FORCE1\n")
                return 3, 1
            force = ':FORCE2'
            if question.find(force) != -1:
                #print("found FORCE2\n")
                return 3, 2
            force = ':FORCE3'
            if question.find(force) != -1:
                #print("found FORCE3\n")
                return 3, 3
            else:
                return 3, 1
        Info = -1
        return False, Info 
    else:
        Info = -1
        return False, Info
    
def run_task_list(task_number, info):
    if task_number == 1:
        print("task 1: COME BACK MODE\n")
        
        response = "おかえりなさい、私の一番好きなお兄ちゃん！"
        VITS_once = True
        AI_emotion = 'happy'
        
        VITS_module_thread = threading.Thread(target=lambda: asyncio.run(VITS.VITS_module(response, VITS_once, "ja")))
        VITS_module_thread.start()

        VTS_module_thread_start = threading.Thread(target=lambda: asyncio.run(VTS.VTS_module(AI_emotion, True)))
        VTS_module_thread_start.start()

        VITS_module_thread.join()

        VTS_module_thread_end = threading.Thread(target=lambda: asyncio.run(VTS.VTS_module(AI_emotion, False)))
        VTS_module_thread_end.start()

        VTS_module_thread_start.join()
        VTS_module_thread_end.join()
        
        
    if task_number == 2:
        print("task 2:END Program!\n")
        sys.exit(0)
    if task_number == 3:
        print("task 3: HUG MODE\n")
        if info == 1:
            print("force 1")
            AI_emotion = 'shy'
            response_list = ["えへへ、お兄ちゃんの体、あったかいです。もっとぎゅってして！"]
            response_list.append("お兄ちゃん、私、あなたに抱かれて本当に嬉しいわ。")
            response_list.append("抱いてくれてありがとう、お兄ちゃん。幸せな気持ちでいっぱいです。")
            response_list.append("この抱擁、本当に暖かいね、お兄ちゃん。大好きだよ。")
            number = random.randint(0, 3)
            response = response_list[number]
        if info == 2:
            print("force 2")
            AI_emotion = 'shy'
            response_list = ["えへへ、お兄ちゃんの体あったかいです。もっとぎゅってして！"]
            response_list.append("離さないで、お兄ちゃん。ずっと、こんな風に近くにいたいな。")
            response_list.append("少し強めの抱擁、気持ちいいな。ありがとう、お兄ちゃん。")
            response_list.append("力強い抱擁、私にとっては安心感があるよ、お兄ちゃん。")
            number = random.randint(0, 3)
            response = response_list[number]
        if info == 3:
            print("force 3")
            AI_emotion = 'mad'
            response_list = ["お兄ちゃん、えんん。きつく抱きしめすぎて少し痛かいですよ"  ]
            response_list.append("お兄ちゃん、抱擁が少し強すぎるかもしれないので、もう少し緩めてもらえますか？")   
            response_list.append("抱擁が強すぎて、息が詰まりそうです。もう少し緩めていただけませんか？")     
            response_list.append("抱擁は好きだけど、今回は少し強すぎました。もう少し優しくしてくれると嬉しいな。")
            number = random.randint(0, 3)
            response = response_list[number]    
        
        VITS_once = True
            
        VITS_module_thread = threading.Thread(target=lambda: asyncio.run(VITS.VITS_module(response, VITS_once, "ja")))
        VITS_module_thread.start()

        VTS_module_thread_start = threading.Thread(target=lambda: asyncio.run(VTS.VTS_module(AI_emotion, True)))
        VTS_module_thread_start.start()

        VITS_module_thread.join()

        VTS_module_thread_end = threading.Thread(target=lambda: asyncio.run(VTS.VTS_module(AI_emotion, False)))
        VTS_module_thread_end.start()

        VTS_module_thread_start.join()
        VTS_module_thread_end.join()
    



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