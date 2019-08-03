import importlib
import threading

gui_module = importlib.import_module("gui_tk")
ping_module = importlib.import_module("ping_script")


# handles calling ping as well as updating the GUI
class PingEngine:
    def __init__(self, runner, gui):
        self.runner = runner
        self.gui = gui

    def start_engine(self):
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

        self.gui.master.title("NA SERVER LEAGUE OF LEGENDS PING")
        self.gui.master.after(500, self.update_ping)
        self.gui.master.after(500, self.calc_avg_ping)
        self.gui.master.mainloop()

    def update_ping(self):
        # checks for new ping info every 50 ms
        update_freq = 100

        if len(self.runner.ping_data) > 0:
            ping_val = self.runner.ping_data[-1]

            if ping_val is not None:
                ping_text = "Ping: " + str(ping_val) + " ms"

                self.gui.ping_info["text"] = ping_text

                self.gui.master.after(update_freq, self.update_ping)
            else:
                self.print_list(self.runner.ping_data)
                print("None!")

    def calc_avg_ping(self):
        update_freq = 100

        total = 0
        if len(self.runner.ping_data) > 0:
            for num in self.runner.ping_data:
                if num is not None:
                    total = total + num

            avg = total / len(self.runner.ping_data)

            avg_string = "%.f" % avg

            ping_text = "Average Ping: " + avg_string + " ms"

            self.gui.avg_ping["text"] = ping_text

            self.gui.master.after(update_freq, self.calc_avg_ping)

    def print_list(self, test_lst):
        for ele in test_lst:
            print(ele)


if __name__ == "__main__":
    main_gui = gui_module.MainGui()
    ping_runner = ping_module.PingRunner()

    engine = PingEngine(ping_runner, main_gui)

    engine.start_engine()
