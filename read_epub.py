import time
from VITS_tools import voice_vits as VITS 

# 指定要打开的EPUB文件的路径
file_path = './imoto.txt'

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()
        # 将文本内容按行分割并逐行打印
        lines = file_contents.splitlines()
        for line in lines:
            if line != '':
                VITS(text=line)
                print(line)
                time.sleep(0.1)
        print(file_contents)

except FileNotFoundError:
    print(f"文件 '{file_path}' 未找到")
except Exception as e:
    print(f"发生错误: {e}")
