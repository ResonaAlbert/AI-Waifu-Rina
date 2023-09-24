import json

def create_json_file(filename, data):
    # 打开文件
    with open(filename, "w") as f:
        # 将数据写入文件
        json.dump(data, f)

if __name__ == "__main__":
    # 指定文件名
    filename = "PersonStatus.json"

    # 指定数据
    data = {"name": "Oniichan",
            "age": 18,
            "time": 12345,
            "heartrate":0,

            "exit":True,
            "last_exit_time":12345,

            "last_talk_time":12345,

            "weather_today":"rain",
            "weather_tomorrow":"rain",
            "news_today":"",

            "face_emotion":"angry"
            }

    # 创建文件并写入数据
    create_json_file(filename, data)
