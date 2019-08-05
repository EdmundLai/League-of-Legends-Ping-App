import threading
# module dependencies in the same folder
import ping_script
import gui_tk


# handles calling ping as well as updating the GUI
class PingEngine:
    def __init__(self):
        self.runner = ping_script.PingRunner()
        self.gui = gui_tk.MainGui()
        self.engine_running = False

    def init_gui(self):
        self.gui.master.title("LEAGUE OF LEGENDS PING")

        self.gui.master.after(0, self.check_engine_start)
        self.gui.master.after(0, self.check_engine_stop)
        self.gui.master.after(100, self.update_ping)
        self.gui.master.after(0, self.calc_avg_ping)
        self.gui.master.after(0, self.update_spikes)

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
        update_interval = 100
        if self.engine_running:
            # checks for new ping info every 100 ms

            if len(self.runner.ping_data) > 0:
                ping_val = self.runner.ping_data[-1]

                ping_text = "Ping: " + str(int(ping_val)) + " ms"

                self.gui.ping_info["text"] = ping_text

        self.gui.master.after(update_interval, self.update_ping)

    def calc_avg_ping(self):
        update_interval = 100
        if self.engine_running:

            total = 0
            if len(self.runner.ping_data) > 0:
                for num in self.runner.ping_data:
                    total = total + num

                avg = total / len(self.runner.ping_data)

                avg_string = "%.f" % avg

                ping_text = "Average Ping: " + avg_string + " ms"

                self.gui.avg_ping["text"] = ping_text

        # calls itself over and over
        self.gui.master.after(update_interval, self.calc_avg_ping)

    def update_spikes(self):
        update_interval = 500
        if self.engine_running:

            spikes = str(self.runner.lag_spikes)

            self.gui.lag_spikes["text"] = "Number of lag spikes: " + spikes

        self.gui.master.after(update_interval, self.update_spikes)

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
