import json
import time
import os

def JSONInfo_update(filename, data_name, Data):
   # Get the absolute path of the current file
   abs_path = os.path.dirname(__file__)
   # Construct the path to the JSON file
   path = os.path.join(abs_path, filename)

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