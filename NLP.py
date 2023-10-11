import asyncio
import google.cloud.language_v1

async def main():
    # 设置你的API密钥
    api_key = 'AIzaSyBpHeNt3QOvAPRjeeKktqgsoHSOIDHI23c'

    # 创建一个客户端
    client = google.cloud.language_v1.LanguageServiceClient(credentials=api_key)

    # 要分析的文本
    text = "这是一段要分析情感的文本。"

    # 调用情感分析API
    document = google.cloud.language_v1.Document(content=text, type_=google.cloud.language_v1.Document.Type.PLAIN_TEXT)
    response = await client.analyze_sentiment(request={'document': document})

    # 获取情感分析结果
    sentiment = response.document_sentiment
    score = sentiment.score
    magnitude = sentiment.magnitude

    # 输出情感分析结果
    print(f'Sentiment score: {score}')
    print(f'Sentiment magnitude: {magnitude}')

    # 根据分数判断情感
    if score > 0:
        print('正面情感')
    elif score < 0:
        print('负面情感')
    else:
        print('中性情感')

asyncio.run(main())
