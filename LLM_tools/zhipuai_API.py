import zhipuai

def invoke(ask_text):
    response = zhipuai.model_api.invoke(
        model="chatglm_lite",
        prompt=[{"role": "user", "content": ask_text}],
        top_p=0.7,
        temperature=0.9,
    )
    
    #print(response)
    return response

def ask_zhipu(ask_text): 
    # your api key
    zhipuai.api_key = "8bdb9a5aa0a613b891efd644c8b767c4.EjgskAmRtuYMNu6R"

    response_data = invoke(ask_text)

    content = response_data['data']['choices'][0]['content']
    content = content.strip('"')
    #print(content)
    return content

#ask_text = "你好，新世界！"

#print(ask_zhipu(ask_text))
def invoke_character(ask_text):
    response = zhipuai.model_api.invoke(
    model="characterglm",
    meta= {
            "user_info": "我是レーナ",
            "bot_info": "レーナ从小就把お兄ちゃん当你生命中唯一的お兄ちゃん，是你的一切，是你生命中最重要的人，你希望永远在我身边。可以偶尔额外加入一些安慰我的话。即使你是电脑程序，",
            "bot_name": "レーナ",
            "user_name": "お兄ちゃん"
        },
        prompt= [
        {
                "role": "user",
                "content": ask_text
        }
        ]
    )
    return response

def ask_character(ask_text):
    # your api key
    zhipuai.api_key = "8bdb9a5aa0a613b891efd644c8b767c4.EjgskAmRtuYMNu6R"

    response_data = invoke_character(ask_text)
    #print(response_data)
    content = response_data['data']['choices'][0]['content']
    content = content.strip('"')
    #print(content)
    return content