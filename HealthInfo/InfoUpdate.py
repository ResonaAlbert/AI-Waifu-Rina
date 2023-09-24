import json
import time
import os

def JSONInfo_update(filename, data_name, Data):
    #abs_path = os.path.dirname(__file__)
    # 打开文件
    #path = os.path.join(abs_path,"PersonStatus.json")
    #path = "./PersonStatus.json"
    with open(filename, "r") as f:
        data = json.load(f)

    # 如果文件不存在，就创建一个
    if not data:
        data = {}

    # 更新数据
    data[data_name] = Data

    # 写入文件
    with open(filename, "w") as f:
        json.dump(data, f)

#TTT = time.time()
#updatejsonfile('PersonStatus.json', "last_talk_time", TTT)

#time.sleep(5)