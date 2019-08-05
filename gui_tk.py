import tkinter as tk


# handles GUI of the Ping Info App
class MainGui:
    def __init__(self):
        self.master = tk.Tk()
        self.master.geometry("400x200+200+200")
        self.master.title("Sample Title")

        self.region = tk.StringVar(self.master)
        self.region.set("NA")
        # regions = ["North America", "Europe West", "Europe North", "Oceania", "Latin America"]
        self.region_select = tk.OptionMenu(self.master, self.region, "NA", "EUW", "EUNE", "OCE", "LAN")
        self.region_select.pack()

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
        self.stop_engine_button.configure(state="disabled")

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
        self.start_engine_button.configure(state="normal")
        self.stop_engine_button.configure(state="disabled")
        self.region_select.configure(state="normal")

    def starting_engine(self):
        # print("engine_start set to true")
        self.engine_start = True
        self.start_engine_button.configure(state="disabled")
        self.stop_engine_button.configure(state="normal")
        self.region_select.configure(state="disabled")

    def get_region(self):
        return self.region.get()



