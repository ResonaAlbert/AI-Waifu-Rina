import tkinter as tk
import time

class TimeApp(tk.Tk):
   def __init__(self):
       super().__init__()
       self.title("Current Time")
       self.geometry("150x50")
       self.create_widgets()

   def create_widgets(self):
       self.time_label = tk.Label(self, text="", font=("Helvetica", 24))
       self.time_label.pack(pady=10)

   def update_time(self):
       current_time = time.strftime("%H:%M:%S")
       self.time_label.config(text=current_time)
       self.after(1000, self.update_time)

if __name__ == "__main__":
   app = TimeApp()
   app.update_time()
   app.mainloop()