import json
import time


def heartrateInfo_update(filename, data):
    # 获取当前时间
    now = time.time()

    # 打开文件
    with open(filename, "r") as f:
        data = json.load(f)

    # 如果文件不存在，就创建一个
    if not data:
        data = {}

    # 更新数据
    data["heartrate"] = data

    # 写入文件
    with open(filename, "w") as f:
        json.dump(data, f)


""" if __name__ == "__main__":
    # 指定文件名
    filename = "PersonStatus.json"

    # 启动一个循环，每隔 5 秒更新一次数据
    while True:
        data = time.localtime
        update_json(filename, data)
        time.sleep(5) """
        
