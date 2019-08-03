import importlib
import threading

gui_module = importlib.import_module("gui_tk")
ping_module = importlib.import_module("ping_script")


# handles calling ping as well as updating the GUI
class PingEngine:
    def __init__(self, runner, gui):
        self.runner = runner
        self.gui = gui
        self.engine_running = False

    def init_gui(self):
        self.gui.master.title("NA SERVER LEAGUE OF LEGENDS PING")

        self.gui.master.after(0, self.check_engine_start)
        self.gui.master.after(0, self.check_engine_stop)
        self.gui.master.after(500, self.update_ping)
        self.gui.master.after(0, self.calc_avg_ping)
        self.gui.master.after(0, self.update_spikes)

        self.gui.master.mainloop()

    def start_engine(self):
        self.engine_running = True

        # IP's found from RIOT Laszlow's Reddit post 3 years ago
        na_server = "104.160.131.3"
        # euw_server = "104.160.141.3"
        # eune_server = "104.160.142.3"
        # oce_server = "104.160.156.1"
        # lan_server = "104.160.136.3"

        # starting thread for ping using cmd
        # only works on windows machines right now
        thread1 = threading.Thread(target=self.runner.run_ping_test, args=(na_server,))
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

                ping_text = "Ping: " + str(ping_val) + " ms"

                self.gui.ping_info["text"] = ping_text

            # calls itself over and over as long as the engine is running

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


if __name__ == "__main__":
    main_gui = gui_module.MainGui()
    ping_runner = ping_module.PingRunner()

    engine = PingEngine(ping_runner, main_gui)

    engine.init_gui()
