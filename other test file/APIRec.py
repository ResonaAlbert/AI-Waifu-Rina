from flask import Flask, request, jsonify

app = Flask(__name__)

# 创建一个空的变量来存储接收到的文本内容
received_text = ""

@app.route('/receive_text', methods=['POST'])
def receive_text():
    global received_text
    data = request.get_json()
    received_text = data.get('text')
    print(received_text)
    return jsonify({'message': 'Text received successfully'})

def process_text(text):
    # 在这里编写处理文本的逻辑
    # 这只是一个示例，你可以根据你的需求进行处理
    return text.upper()  # 这里示例将文本转换为大写

@app.route('/get_result', methods=['GET'])
def get_result():
    global received_text
    # 在这里处理接收到的文本内容，并返回结果
    # 这只是一个示例，你可以根据你的需求进行处理
    result = process_text(received_text)
    return jsonify({'result': result})

#if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000)
