import json
import asyncio
import websockets
import subprocess
import time
from InfoUpdate import JSONInfo_update
import os

# 指定要运行的可执行文件的路径
# 获取当前文件夹的路径
#current_dir = os.getcwd()
# 获取上级文件夹的路径
#parent_dir = os.path.dirname(current_dir)
#print(parent_dir)
# 获取上级文件夹中的另一个文件夹的路径
#other_dir = parent_dir+'\\vts-heartrate\\vts-heartrate.exe'
#print(other_dir)
exe_path = "./vts-heartrate/vts-heartrate.exe"

# 启动可执行文件
process = subprocess.Popen(exe_path)
time.sleep(30)
print("Waiting for 30 seconds is over.")

async def websocket_client():
    print("start heart rate update")
    global END_heartrate_update
    uri = "ws://localhost:8214/data"
    time_now = time.time()  # 设置时间间隔为5秒
    time_last = 0  # 记录上次接收数据的时间
    heartrate_old2 = 0
    heartrate_old1 = 0    
    async with websockets.connect(uri) as websocket:
        while True:
           # if END_heartrate_update == True:
           #     break
            try:
                message = await websocket.recv()
                data_dict = json.loads(message)
                heartrate = data_dict['data']['heartrate']

                if heartrate_old1 != heartrate:
                    print(heartrate_old1)
                    heartrate_old1 = heartrate
                    heartrate_old2 = heartrate_old1
                    #time_last = time_now
                    time_now = time.time()

                if (time_now - time_last) > 5 & (heartrate_old1 - heartrate_old2) != 0 :
                    #print(f"Heart rate now: {heartrate_old1}")
                    JSONInfo_update("PersonStatus.json", "heartrate", heartrate_old1)
                    time_last = time.time()
                
                #print(message)
                #await asyncio.sleep(1)  # 每秒检查一次，以避免阻塞
                
            except websockets.exceptions.ConnectionClosed:
                print("WebSocket connection closed.")
                break

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(websocket_client())
    END_heartrate_update = False

