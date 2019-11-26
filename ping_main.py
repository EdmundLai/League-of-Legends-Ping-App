import threading
import ping_script
import gui_tk


# handles calling ping as well as updating the GUI
class PingEngine:
    def __init__(self):
        self.runner = ping_script.PingRunner()
        self.gui = gui_tk.MainGui()
        self.engine_running = False
        self.current_ping_tuple = None
        self.latency_status = None
        self.stability_status = None

    def init_engine(self):
        self.init_gui()

    def init_gui(self):
        self.gui.master.title("League of Legends Ping Test")

        self.gui.master.after(0, self.check_engine_start)
        self.gui.master.after(0, self.check_engine_stop)
        self.gui.master.after(100, self.check_update_data)

        self.gui.start_animation()

        self.gui.master.mainloop()

    def start_engine(self):
        self.engine_running = True

        # IP's found from RIOT Laszlow's Reddit post 3 years ago
        selected_region = self.gui.get_region()

        # print(selected_region)

        if selected_region == "NA":
            server = "104.160.131.3"
        elif selected_region == "EUW":
            server = "104.160.141.3"
        elif selected_region == "EUNE":
            server = "104.160.142.3"
        elif selected_region == "OCE":
            server = "104.160.156.1"
        # LAN server
        else:
            server = "104.160.136.3"

        # starting thread for ping using terminal
        thread1 = threading.Thread(target=self.runner.run_ping_test, args=(server,))
        thread1.daemon = True
        thread1.start()

    def stop_engine(self):
        self.engine_running = False
        self.runner.stop_thread = True
        self.gui.reset_info()

    def update_ping(self):
        current_ping = self.current_ping_tuple[1]

        ping_text = "Ping: " + str(int(current_ping)) + " ms"

        self.gui.ping_info["text"] = ping_text

    def calc_avg_ping(self):
        total = 0

        for curr_tuple in self.runner.ping_data:
            ping_value = curr_tuple[1]
            total = total + ping_value

        avg_ping = total / len(self.runner.ping_data)

        avg_ping_string = "%.f" % avg_ping

        ping_text = "Average Ping: " + avg_ping_string + " ms"

        self.gui.avg_ping["text"] = ping_text

    def update_spikes(self):
        spikes = str(self.runner.lag_spikes)

        self.gui.lag_spikes["text"] = "Number of lag spikes: " + spikes

    def update_ping_diff(self):
        if self.runner.ping_diff is not None:
            diff = str(int(round(self.runner.ping_diff)))

            self.gui.ping_diff["text"] = "Difference between last 2 ping values: " + diff + " ms"

    def update_latency(self):
        status_types = ["LOW", "MEDIUM", "HIGH", "VERY HIGH"]

        current_ping = self.current_ping_tuple[1]

        if current_ping < 60:
            self.latency_status = status_types[0]
        elif current_ping < 100:
            self.latency_status = status_types[1]
        elif current_ping < 200:
            self.latency_status = status_types[2]
        else:
            self.latency_status = status_types[3]

        latency_text = "Latency: " + self.latency_status

        self.gui.latency["text"] = latency_text

    def update_stability(self):
        status_types = ["STABLE", "UNSTABLE"]

        # print(self.runner.time_no_lag)

        if self.runner.lag_spikes == 0:
            self.stability_status = status_types[0]
        else:
            # if in the last minute there have been no ping spikes, the connection is stable
            if self.runner.time_no_lag > 60:
                self.stability_status = status_types[0]
            else:
                self.stability_status = status_types[1]

        stability_text = "Stability: " + self.stability_status

        self.gui.stability["text"] = stability_text

    # makes a recommendation for optimal gaming experience depending on current connection quality
    def make_recommendation(self):
        # print(self.stability_status)
        # print(self.latency_status)
        # if self.stability_status == "STABLE":
        #     print("connection is stable!")
        #
        # if self.latency_status == "MEDIUM":
        #     print("latency is okay!")
        # else:
        #     print("latency is not okay!")

        if self.stability_status == "STABLE" and (self.latency_status == "LOW" or self.latency_status == "MEDIUM"):
            recommendation = "YES"
        else:
            recommendation = "NO"

        recommendation_text = "Can I play League right now? " + recommendation

        self.gui.recommendation["text"] = recommendation_text

    def check_engine_start(self):
        update_interval = 100

        if self.gui.engine_start:
            self.gui.engine_start = False

            if not self.engine_running:
                # print("Engine starting!")
                self.start_engine()

        self.gui.master.after(update_interval, self.check_engine_start)

    def check_engine_stop(self):
        update_interval = 100

        if self.gui.engine_stop:
            self.gui.engine_stop = False

            if self.engine_running:
                # print("Engine stopping!")
                self.stop_engine()

        self.gui.master.after(update_interval, self.check_engine_stop)

    # update the gui whenever new data arrives, checks every 100 ms
    def check_update_data(self):
        update_interval = 100

        if self.engine_running:
            if self.runner.data_changed:
                self.runner.data_changed = False

                # updating current ping if there is any data
                if len(self.runner.ping_data) > 0:
                    self.current_ping_tuple = self.runner.ping_data[-1]

                    self.calc_avg_ping()
                    self.update_ping()
                    self.update_spikes()
                    self.update_ping_diff()
                    self.update_latency()
                    self.update_stability()
                    self.make_recommendation()
                    # self.runner.show_ping_data()
                    time_ping_tup = PingEngine.convert_to_lists(self.runner.ping_data)

                    self.gui.update_data(time_ping_tup)

        self.gui.master.after(update_interval, self.check_update_data)

    @staticmethod
    def convert_to_lists(ping_data):
        time_list = []
        ping_list = []
        for current_tup in ping_data:
            time_list.append(current_tup[0])
            ping_list.append(current_tup[1])

        return time_list, ping_list
