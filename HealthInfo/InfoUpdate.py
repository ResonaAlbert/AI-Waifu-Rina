import json
import time
import os
import numpy as np
    
def JSONInfo_update(filename, data_name, Data):
   # Get the absolute path of the current file
   abs_path = os.path.dirname(__file__)
   # Get the absolute path of the JSON file without the filename
   path_without_filename = os.path.dirname(abs_path)
   # Construct the path to the JSON file
   path = os.path.join(path_without_filename, filename)

   # Open the JSON file in read mode
   with open(path, "r") as f:
       # Load the JSON data
       data = json.load(f)

   # If the JSON data is empty, create an empty dictionary
   if not data:
       data = {}

   # Update the data
   data[data_name] = Data

   # Write the updated JSON data to the file
   with open(path, "w") as f:
       json.dump(data, f)

# Update the "last_talk_time" value in the "PersonStatus.json" file
#TTT = time.time()
#updatejsonfile('PersonStatus.json', "last_talk_time", TTT)

# Sleep for 5 seconds
# time.sleep(5)

def JSONInfo_get(json_file_path, data_name):
    """
    从指定json文件获取指令label的值

    Args:
        json_file_path: 指定json文件的路径

    Returns:
        指令label的值
    """

    # 打开json文件
    with open(json_file_path, "r") as f:
        data = json.load(f)

    # 获取指令label的值
    return data[data_name]

def AI_daily_emotion_gen():
    JloveValue = JSONInfo_get('./PersonStatus.json', "loveValue")
    emotion_probility  = np.random.uniform(1, 0)
    if JloveValue > 50:
        if emotion_probility > 0.3:
            AI_daily_emotion = "positive"
        else:
            AI_daily_emotion = "negative"
    else:
        if emotion_probility > 0.7:
            AI_daily_emotion = "positive"
        else:
            AI_daily_emotion = "negative"
    JSONInfo_update('./PersonStatus.json', "AI_daily_emotion", AI_daily_emotion)