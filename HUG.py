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
        #print(value)
        int_value = int(value)
        if value == "unavailable":
            return 0
        else:
            return int_value
    else:
        return 0

def send_command(Force):
    # 将内容转换为 json 格式
    if Force == 1:
        data = {'text': "COMMAND:HUG:FORCE1"}
    if Force == 2:
        data = {'text': "COMMAND:HUG:FORCE2"}    
    if Force == 3:
        data = {'text': "COMMAND:HUG:FORCE3"}
    else:
        data = {'text': "COMMAND:HUG:FORCE1"}

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
    HUG_status = 0
    while True:
        value = get_sensor_value()
        value = value/100000
        if value < 8:
            if HUG_status != 0:
                T = time.time() - reaction_time
                if T > 20:
                    HUG_status = 0
                    print('hug mode stop!')


        if value > 10:
            if HUG_status == 0:
                    # start
                    HUG_status = 1
                    reaction_time = time.time()
                    print('hug mode start!')
                    print('force 1')
                    send_command(1)
        if value > 20:
            if HUG_status == 1:
                T = time.time() - reaction_time
                if T > 20:
                    HUG_status = 2
                    send_command(2)
                    print('force 2')
                    reaction_time = time.time()
        if value > 25:
            if HUG_status == 2:
                T = time.time() - reaction_time
                if T > 20:
                    HUG_status = 2
                    send_command(3)
                    print('force 3')
                    reaction_time = time.time()   
        time.sleep(5)     





