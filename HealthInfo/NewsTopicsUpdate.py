import json
import urllib.request
import time
from InfoUpdate import JSONInfo_update

# 定义一个函数news_get，用于获取新闻数据
def news_get(url):
   # 使用urllib.request.urlopen函数打开url，并将响应结果以json格式读取
   with urllib.request.urlopen(url) as response:
       data = json.loads(response.read().decode("utf-8"))
       # 从data中获取articles，并赋值给articles
       articles = data["articles"]
       # 返回articles
       return articles

# 定义一个函数update_news，用于更新新闻数据
def update_news(url, category, index):
   # 调用news_get函数，获取新闻数据
   articles = news_get(url)
   # 从articles中获取title，并赋值给title
   title = articles[index]['title']
   # 从articles中获取content，并赋值给content
   content = articles[index]['description']
   # 调用JSONInfo_update函数，更新topic.json文件中news1的title
   JSONInfo_update(f'topic.json', f'news{index} title', title)
   # 调用JSONInfo_update函数，更新topic.json文件中news1的content
   JSONInfo_update(f'topic.json', f'news{index} content', content)
   # 调用JSONInfo_update函数，更新topic.json文件中news1的status
   JSONInfo_update(f'topic.json', f'news{index} status', True)

# 定义apikey，category1，category2，category3，category4，用于存储API密钥、类别、类别2、类别3、类别4
apikey = "80e8deeabdb65c7f200ae87fec302f08"
category1 = "general"
category2 = "nation"
category3 = "world"
category4 = "technology"

# 定义urls，用于存储类别和url
urls = {
   category1: f"https://gnews.io/api/v4/top-headlines?category={category1}&lang=zh&country=cn&max=10&apikey={apikey}",
   category2: f"https://gnews.io/api/v4/top-headlines?category={category2}&lang=zh&country=cn&max=10&apikey={apikey}",
   category3: f"https://gnews.io/api/v4/top-headlines?category={category3}&lang=zh&country=cn&max=10&apikey={apikey}",
   category4: f"https://gnews.io/api/v4/top-headlines?category={category4}&lang=zh&country=cn&max=10&apikey={apikey}"
}

# 遍历urls，调用update_news函数，更新新闻数据
for category, url in urls.items():
   update_news(url, category, 1)  # 更新 news1
   time.sleep(3)  # 等待一段时间，以避免 API 限制
   update_news(url, category, 2)  # 更新 news2
   time.sleep(3)  # 等待一段时间，以避免 API 限制
   update_news(url, category, 3)  # 更新 news3import json
   update_news(url, category, 3)  # 更新 news3