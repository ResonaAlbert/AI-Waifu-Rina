import requests
import datetime
import json

# 获取 API 密钥
API_KEY = "914e8400f7d8625796b5464151703f6b"

# 设置城市名称
CITY_NAME = "Milan"
today = datetime.datetime.today()
tomorrow = today + datetime.timedelta(days=1)
today_string = today.strftime("%Y-%m-%d")
tomorrow_string = tomorrow.strftime("%Y-%m-%d")

# 构建请求 URL
URL1 = "https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={lon}&lang=zh_cn&date={date}&units=metric&appid=914e8400f7d8625796b5464151703f6b".format(
   lat=45.28, lon=9.1,  date=today_string
)
URL2 = "https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={lon}&lang=zh_cn&date={date}&units=metric&appid=914e8400f7d8625796b5464151703f6b".format(
   lat=45.28, lon=9.1,  date=tomorrow_string
)

# 发送请求
response1 = requests.get(URL1)
   # 检查响应
if response1.status_code != 200:
   raise Exception(
       "Error fetching weather data. Code: {}. Content: {}".format(
           response1.status_code, response1.content
       )
   )
response2 = requests.get(URL2)
# 检查响应
if response2.status_code != 200:
   raise Exception(
       "Error fetching weather data. Code: {}. Content: {}".format(
           response2.status_code, response2.content
       )
   )

def Update_WeatherInfo(response, data_date):

   # 解析响应
   data = [0, 0, 0, 0, 0]
   weather_data = response.json()
   data[0] = weather_data["temperature"]["min"]
   data[1] = weather_data["temperature"]["max"]
   data[2] = weather_data["precipitation"]["total"]
   data[3] = weather_data["cloud_cover"]["afternoon"]
   data[4] = weather_data["humidity"]["afternoon"]

   # 打印天气信息
   # print(weather_data)

   # 读取 JSON 数据
   with open("topic.json", "r") as f:
       json_data = json.load(f)

   # 修改 speed 值
   json_data[data_date]["temperature_min"] = data[0]
   json_data[data_date]["temperature_max"] = data[1]
   json_data[data_date]["precipitation"] = data[2]
   json_data[data_date]["cloud_cover"] = data[3]
   json_data[data_date]["humidity"] = data[4]

   # 将 JSON 数据转换为字符串
   json_string = json.dumps(json_data)

   # 保存 JSON 数据到文件
   with open("topic.json", "w") as f:
       f.write(json_string)

data_date = "weather today"
Update_WeatherInfo(response1, data_date)
data_date = "weather tomorrow"
Update_WeatherInfo(response2, data_date)

""" 2023-09-24
{'lat': 45.28, 
'lon': 9.1, 
'tz': '+02:00', 
'date': '2023-09-24', 
'units': 'metric',
'cloud_cover': {'afternoon': 0.0}, 
'humidity': {'afternoon': 53.81}, 
'precipitation': {'total': 0.0}, 
'temperature': {'min': 11.53, 
'max': 21.93, 
'afternoon': 18.97, 
'night': 13.76, 
'evening': 21.25, 
'morning': 11.85}, 
'pressure': {'afternoon': 1021.8}, 
'wind': {'max': {'speed': 2.38, 'direction': 332.8}}}
 """