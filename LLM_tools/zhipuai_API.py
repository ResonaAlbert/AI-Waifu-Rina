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