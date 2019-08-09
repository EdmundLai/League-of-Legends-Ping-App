import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# handles GUI of the Ping Info App
class MainGui:
    def __init__(self):
        self.master = tk.Tk()
        self.master.geometry("800x600+400+400")
        self.master.title("Sample Title")

        # initializing region select dropdown menu
        self.region = tk.StringVar(self.master)
        self.region.set("NA")
        # regions = ["North America", "Europe West", "Europe North", "Oceania", "Latin America"]
        self.region_select = tk.OptionMenu(self.master, self.region, "NA", "EUW", "EUNE", "OCE", "LAN")
        self.region_select.pack()

        # initializing current ping label
        self.ping_info = tk.Label(self.master, text="Ping: N/A ms")
        self.ping_info.pack()

        # initializing average ping label
        self.avg_ping = tk.Label(self.master, text="Average Ping: N/A ms")
        self.avg_ping.pack()

        # initializing the matplotlib graph
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.a = self.figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(self.figure, self.master)
        canvas.get_tk_widget().pack()

        self.time_data = []
        self.ping_data = []
        self.a.plot(self.time_data, self.ping_data)

        # times the cmd ping request times out
        self.lag_spikes = tk.Label(self.master, text="Number of lag spikes: 0")
        self.lag_spikes.pack()

        # start button init
        self.start_engine_button = tk.Button(self.master, text="Start Test", command=self.starting_engine)
        self.start_engine_button.pack()

        # stop button init
        self.stop_engine_button = tk.Button(self.master, text="Stop Test", command=self.stopping_engine)
        self.stop_engine_button.pack()
        self.stop_engine_button.configure(state="disabled")

        # requests for Ping runner to be started
        self.engine_start = False

        # requests for PingRunner to be stopped
        self.engine_stop = False

    # Reinitializing GUI information to default states
    def reset_info(self):
        self.ping_info["text"] = "Ping: N/A ms"
        self.avg_ping["text"] = "Average Ping: N/A ms"
        self.lag_spikes["text"] = "Number of lag spikes: 0"

    # Gets GUI ready allow user to start the ping test
    def stopping_engine(self):
        self.engine_stop = True
        self.start_engine_button.configure(state="normal")
        self.stop_engine_button.configure(state="disabled")
        self.region_select.configure(state="normal")

    # Gets GUI ready to allow user to stop the ping test
    def starting_engine(self):
        self.engine_start = True
        self.start_engine_button.configure(state="disabled")
        self.stop_engine_button.configure(state="normal")
        self.region_select.configure(state="disabled")

    def get_region(self):
        return self.region.get()

    # updating GUI info with current values from MySQL database
    def update_data(self, time_ping_tuple):
        self.time_data = time_ping_tuple[0]
        self.ping_data = time_ping_tuple[1]

    # calls animate every 100 ms
    def start_animation(self):
        self.anim = animation.FuncAnimation(self.figure, self.animate, interval=100)
        plt.show()

    # plots the current time and ping data
    def animate(self, i):
        self.a.clear()
        self.a.plot(self.time_data, self.ping_data)
