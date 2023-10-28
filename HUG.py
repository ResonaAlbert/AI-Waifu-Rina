import requests
import time
import json

def get_sensor_value():
    """获取 Home Assistant 中 sensor.esphome_web_dcdf28_hx711_value 的数值。"""

    url = "http://192.168.1.236:8123/api/states/sensor.esphome_web_dcdf28_hx711_value"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlNzE1OWYxNzAwNTk0ZDIxODU4OTI5YmQ3NjExZWFmOCIsImlhdCI6MTY5ODUyOTYxNCwiZXhwIjoyMDEzODg5NjE0fQ.e0veWiZvcRAF821ZBroQxLksnoCDBNeMA4Ps7hGrCiE",
        "content-type": "application/json",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        value = data['state']
        print(value)
        int_value = int(value)
        if value == "unavailable":
            return 0
        else:
            return int_value
    else:
        return 0

def send_command():
    # 将内容转换为 json 格式
    data = {'text': "COMMAND:HUG"}
    api_url_receive = 'http://localhost:56789/receive_text'
    # 发送请求
    response = json
    response = requests.post(api_url_receive, json=data)

    # 检查响应状态码
    if response.status_code == 200:
        # 响应成功
        print("发送成功！")
    else:
        # 响应失败
        print("发送失败！")

if __name__ == "__main__":
    while True:
        value = get_sensor_value()
        time.sleep(10)
        if value > 843348:
            print(value)
            send_command()

