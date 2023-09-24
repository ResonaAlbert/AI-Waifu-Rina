# https://docs.python.org/3/library/json.html
# This library will be used to parse the JSON data returned by the API.
import json
# https://docs.python.org/3/library/urllib.request.html#module-urllib.request
# This library will be used to fetch the API.
import urllib.request
import time
from InfoUpdate import JSONInfo_update

import datetime

today = datetime.date.today()
JSONInfo_update('topic.json', "data", str(today))

apikey = "80e8deeabdb65c7f200ae87fec302f08"
category1 = "general"
category2 = "nation"
category3 = "world"
category4 = "technology"

url1 = f"https://gnews.io/api/v4/top-headlines?category={category1}&lang=zh&country=cn&max=10&apikey={apikey}"
url2 = f"https://gnews.io/api/v4/top-headlines?category={category2}&lang=zh&country=cn&max=10&apikey={apikey}"
url3 = f"https://gnews.io/api/v4/top-headlines?category={category3}&lang=zh&country=cn&max=10&apikey={apikey}"
url4 = f"https://gnews.io/api/v4/top-headlines?category={category4}&lang=zh&country=cn&max=10&apikey={apikey}"

def news_get(url):
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]

        for i in range(len(articles)):
            print(i)
            # articles[i].title
            print(f"Title: {articles[i]['title']}")
            # articles[i].description
            print(f"Description: {articles[i]['description']}") 

            # You can replace {property} below with any of the article properties returned by the API.
            # articles[i].{property}
            # print(f"{articles[i]['{property}']}")
            # Delete this line to display all the articles returned by the request. Currently only the first article is displayed.
            break

    return articles

time.sleep(3)
data = news_get(url1)
title = data[0]['title']
content = data[0]['description']
JSONInfo_update('topic.json', "news1 title", title)
JSONInfo_update('topic.json', "news1 content", content)
JSONInfo_update('topic.json', "news1 status", True)

time.sleep(3)
news_get(url2)
title = data[0]['title']
content = data[0]['description']
JSONInfo_update('topic.json', "news2 title", title)
JSONInfo_update('topic.json', "news2 content", content)
JSONInfo_update('topic.json', "news2 status", True)
time.sleep(3)
news_get(url3)
title = data[0]['title']
content = data[0]['description']
JSONInfo_update('topic.json', "news3 title", title)
JSONInfo_update('topic.json', "news3 content", content)
JSONInfo_update('topic.json', "news3 status", True)
time.sleep(3)
news_get(url4)
title = data[0]['title']
content = data[0]['description']
JSONInfo_update('topic.json', "news3 title", title)
JSONInfo_update('topic.json', "news3 content", content)
JSONInfo_update('topic.json', "news3 status", True)

# 解码 JSON 字符串
""" with open('topic.json', "r") as f:
    data = json.load(f)
# 获取新闻标题
title = data["news1 title"]
print(title) """


