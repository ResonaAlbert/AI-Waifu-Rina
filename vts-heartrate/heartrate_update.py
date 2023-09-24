import json
import asyncio
import websockets
import subprocess
import time
from HealthInfo.InfoUpdate import JSONInfo_update


# 指定要运行的可执行文件的路径
exe_path = "./vts-heartrate.exe"
# 启动可执行文件
process = subprocess.Popen(exe_path)
time.sleep(10)
print("Waiting for 10 seconds is over.")

async def websocket_client():
    global END_heartrate_update
    uri = "ws://localhost:8214/data"
    time_now = 0  # 设置时间间隔为5秒
    time_last = 0  # 记录上次接收数据的时间
    heartrate_old = 0    
    async with websockets.connect(uri) as websocket:
        while True:
            if END_heartrate_update == True:
                break
            try:
                message = await websocket.recv()
                data_dict = json.loads(message)
                heartrate = data_dict['data']['heartrate']
                if heartrate_old != heartrate:
                    heartrate_old = heartrate
                    time_last = time_now
                    time_now = time.time()

                if (time_now - time_last) > 5:
                    print(f"Heart rate now: {heartrate_old}")
                    JSONInfo_update("PersonStatus", "heartrate", heartrate_old)
                
                #print(message)
                await asyncio.sleep(1)  # 每秒检查一次，以避免阻塞
                
            except websockets.exceptions.ConnectionClosed:
                print("WebSocket connection closed.")
                break

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(websocket_client())
    END_heartrate_update = False

