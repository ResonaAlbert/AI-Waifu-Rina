import json
import asyncio
import websockets
import subprocess
import time
from InfoUpdate import JSONInfo_update
import os

exe_path = "./vts-heartrate/vts-heartrate.exe"

# Start the executable file
process = subprocess.Popen(exe_path)
time.sleep(30)
print("Waiting for 30 seconds is over.")

# Create a websocket connection
async def websocket_client():
   print("Start heart rate update")
   global END_heartrate_update
   uri = "ws://localhost:8214/data"
   time_now = time.time()  # Set time interval to 5 seconds
   time_last = 0  # Record the last received data time
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

               if (time_now - time_last) > 5 and (heartrate_old1 - heartrate_old2) != 0:
                   #print(f"Heart rate now: {heartrate_old1}")
                   JSONInfo_update("PersonStatus.json", "heartrate", heartrate_old1)
                   time_last = time.time()

               #print(message)
               #await asyncio.sleep(1)  # Check every second to avoid blocking

           except websockets.exceptions.ConnectionClosed:
               print("WebSocket connection closed.")
               break

if __name__ == "__main__":
   asyncio.get_event_loop().run_until_complete(websocket_client())
   END_heartrate_update = False