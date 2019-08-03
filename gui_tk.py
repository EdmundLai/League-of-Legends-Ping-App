import tkinter as tk


# handles GUI of the Ping Info App
class MainGui:
    def __init__(self):
        self.master = tk.Tk()
        self.master.geometry("400x50+200+200")
        self.master.title("Sample Title")

        self.ping_info = tk.Label(self.master, text="Ping: N/A ms")
        self.ping_info.pack()

        self.avg_ping = tk.Label(self.master, text="Average Ping: N/A ms")
        self.avg_ping.pack()
