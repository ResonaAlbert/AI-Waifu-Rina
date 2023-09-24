import requests
import json

# 定义API的URL
api_url_receive = 'http://localhost:2907/receive_text'

# 要发送的文本内容
text_to_send = {'text': '这是要发送的文本内容'}

# 发送POST请求 bug json cannot receive
data = json
data  = requests.post(api_url_receive, json=text_to_send)

# 检查响应状态码
if data.status_code == 200:
    # 响应成功
    print("发送成功！")
else:
    # 响应失败
    print("发送失败！")