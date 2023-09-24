import requests
import json
# 获取命令行输入的内容
api_url_receive = 'http://localhost:56789/receive_text'
while True:
    content = input('请输入内容：')

    # 将内容转换为 json 格式
    data = {'text': content}

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
