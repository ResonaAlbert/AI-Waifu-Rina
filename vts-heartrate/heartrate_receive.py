import json
import asyncio
import websockets
import subprocess
import time

# 指定要运行的可执行文件的路径
exe_path = "./vts-heartrate.exe"

# 启动可执行文件
process = subprocess.Popen(exe_path)

# 等待10秒钟
time.sleep(10)

# 可以选择等待进程完成
# process.wait()

# 打印一条消息来指示等待已经完成
print("Waiting for 10 seconds is over.")

async def websocket_client():
    uri = "ws://localhost:8214/data"
    interval = 5  # 设置时间间隔为5秒
    last_receive_time = 0  # 记录上次接收数据的时间
    heartrate_old = 0    
    async with websockets.connect(uri) as websocket:
        while True:
            try:
                message = await websocket.recv()
                data_dict = json.loads(message)
                heartrate = data_dict['data']['heartrate']
                if heartrate_old != heartrate:
                    heartrate_old = heartrate
                    print(f"Heart rate: {heartrate_old}")
                # print(f"Heart rate: {heartrate}")
                #print(message)
                #await asyncio.sleep(1)  # 每秒检查一次，以避免阻塞
                
            except websockets.exceptions.ConnectionClosed:
                print("WebSocket connection closed.")
                break

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(websocket_client())
