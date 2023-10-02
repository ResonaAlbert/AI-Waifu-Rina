from flask import Flask, request
import json

app = Flask(__name__)
app.run(host='0.0.0.0', port=56789)

@app.route('/receive_text', methods=['POST'])
def receive_text():
    # 获取 POST 请求的参数
    data = request.get_json()

    # 打印参数
    received_text = data.get('text')

    reply = {"message": "Question received successfully"}
    # 将返回信息转换为json格式
    reply_json = json.dumps(reply)
    # 返回json格式的信息
    return reply_json

if __name__ == '__main__':
    app.run()


