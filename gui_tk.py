import tkinter as tk


# handles GUI of the Ping Info App
class MainGui:
    def __init__(self):
        self.master = tk.Tk()
        self.master.geometry("400x200+200+200")
        self.master.title("Sample Title")

        self.ping_info = tk.Label(self.master, text="Ping: N/A ms")
        self.ping_info.pack()

        self.avg_ping = tk.Label(self.master, text="Average Ping: N/A ms")
        self.avg_ping.pack()

        self.lag_spikes = tk.Label(self.master, text="Number of lag spikes: 0")
        self.lag_spikes.pack()

        self.start_engine_button = tk.Button(self.master, text="Start Test", command=self.starting_engine)
        self.start_engine_button.pack()

        self.stop_engine_button = tk.Button(self.master, text="Stop Test", command=self.stopping_engine)
        self.stop_engine_button.pack()

        # requests for Ping runner to be started
        self.engine_start = False

        # requests for PingRunner to be stopped
        self.engine_stop = False

    def reset_info(self):
        self.ping_info["text"] = "Ping: N/A ms"
        self.avg_ping["text"] = "Average Ping: N/A ms"
        self.lag_spikes["text"] = "Number of lag spikes: 0"

    def stopping_engine(self):
        # print("engine_stop set to true")
        self.engine_stop = True

    def starting_engine(self):
        # print("engine_start set to true")
        self.engine_start = True



