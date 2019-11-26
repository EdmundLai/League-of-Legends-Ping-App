import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use("TkAgg")


# handles GUI of the Ping Info App
class MainGui:
    def __init__(self):
        self.master = tk.Tk()
        self.master.geometry("750x450")

        stats_frame = tk.Frame(self.master, width=600, height=400)

        graph_frame = tk.Frame(self.master, width=600, height=400)

        stats_frame.grid(row=0, column=0, padx=20, pady=20)
        graph_frame.grid(row=0, column=1, padx=20, pady=20)

        buttons_frame = tk.Frame(stats_frame, width=200, height=50)
        region_frame = tk.Frame(stats_frame)
        ping_frame = tk.Frame(stats_frame)
        connection_frame = tk.Frame(stats_frame)

        region_frame.grid(row=0, pady=20)
        buttons_frame.grid(row=1, pady=20)
        ping_frame.grid(row=2, pady=20)
        connection_frame.grid(row=3, pady=20)

        # initializing region select dropdown menu
        self.region_label = tk.Label(region_frame, text="Select Region:")
        self.region_label.grid(row=0, column=0, padx=5)
        self.region = tk.StringVar(region_frame)
        self.region.set("NA")
        # regions = ["North America", "Europe West", "Europe North", "Oceania", "Latin America"]
        self.region_select = tk.OptionMenu(region_frame, self.region, "NA", "EUW", "EUNE", "OCE", "LAN")
        self.region_select.grid(row=0, column=1, padx=5)

        # start button init
        self.start_engine_button = tk.Button(buttons_frame, text="Start Test", command=self.starting_engine)
        self.start_engine_button.grid(row=0, column=0, padx=5)
        # stop button init
        self.stop_engine_button = tk.Button(buttons_frame, text="Stop Test", command=self.stopping_engine)
        self.stop_engine_button.grid(row=0, column=1, padx=5)
        self.stop_engine_button.configure(state="disabled")

        # initializing current ping label
        self.ping_info = tk.Label(ping_frame, text="Ping: N/A ms")
        self.ping_info.pack()

        # initializing average ping label
        self.avg_ping = tk.Label(ping_frame, text="Average Ping: N/A ms")
        self.avg_ping.pack()

        # for debugging purposes only
        self.ping_diff = tk.Label(ping_frame, text="Difference between last 2 ping values: N/A ms")
        # self.ping_diff.pack()

        # times the cmd ping request times out
        self.lag_spikes = tk.Label(ping_frame, text="Number of lag spikes: 0")
        self.lag_spikes.pack()

        # initializing the matplotlib graph
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.a = self.figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(self.figure, graph_frame)
        canvas.get_tk_widget().pack()

        self.time_data = []
        self.ping_data = []
        self.a.plot(self.time_data, self.ping_data)

        # requests for Ping runner to be started
        self.engine_start = False

        # requests for PingRunner to be stopped
        self.engine_stop = False

        # connection quality label
        self.conn_quality = tk.Label(connection_frame, text="Connection Quality Information:")
        self.conn_quality.pack()

        # dependent on current_ping
        # can be ranked from low, medium, high, very high
        # high and very high are unplayable
        self.latency = tk.Label(connection_frame, text="Latency: UNKNOWN")
        self.latency.pack()

        # dependent on number of ping spikes > 5 (can be changed)
        # can be classified into stable and unstable
        # unstable is unplayable
        self.stability = tk.Label(connection_frame, text="Stability: UNKNOWN")
        self.stability.pack()

        self.recommendation = tk.Label(connection_frame, text="Can I play League right now? N/A")

    # Reinitializing GUI information to default states
    def reset_info(self):
        self.ping_info["text"] = "Ping: N/A ms"
        self.avg_ping["text"] = "Average Ping: N/A ms"
        self.lag_spikes["text"] = "Number of lag spikes: 0"
        self.ping_diff["text"] = "Difference between last 2 ping values: N/A ms"
        self.latency["text"] = "Latency: UNKNOWN"
        self.stability["text"] = "Stability: UNKNOWN"
        self.recommendation["text"] = "Can I play League right now? N/A"

    # Gets GUI ready allow user to start the ping test
    def stopping_engine(self):
        self.engine_stop = True
        self.start_engine_button.configure(state="normal")
        self.stop_engine_button.configure(state="disabled")
        self.region_select.configure(state="normal")
        self.recommendation.pack_forget()

    # Gets GUI ready to allow user to stop the ping test
    def starting_engine(self):
        self.engine_start = True
        self.start_engine_button.configure(state="disabled")
        self.stop_engine_button.configure(state="normal")
        self.region_select.configure(state="disabled")
        self.recommendation.pack()

    def get_region(self):
        return self.region.get()

    # updating GUI info with current values from the Engine
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
        self.a.set_title("Ping to League Server")
        self.a.set_xlabel("Time (seconds)")
        self.a.set_ylabel("Ping (milliseconds)")
        self.a.plot(self.time_data, self.ping_data)
