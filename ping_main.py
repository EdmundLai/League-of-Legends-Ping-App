import threading
import ping_script
import gui_tk
import mysql_mod


# handles calling ping as well as updating the GUI
class PingEngine:
    def __init__(self):
        self.runner = ping_script.PingRunner()
        self.gui = gui_tk.MainGui()
        self.sql_module = mysql_mod.MySQLModule()
        self.engine_running = False
        self.current_ping_tuple = None

    def init_engine(self):
        self.init_mysql()
        self.init_gui()

    def init_mysql(self):
        self.sql_module.init_database()

    def init_gui(self):
        self.gui.master.title("LEAGUE OF LEGENDS PING")

        self.gui.master.after(0, self.check_engine_start)
        self.gui.master.after(0, self.check_engine_stop)
        self.gui.master.after(100, self.check_update_data)

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
        self.init_mysql()

    def update_ping(self):
        current_ping = self.current_ping_tuple[1]

        ping_text = "Ping: " + str(int(current_ping)) + " ms"

        self.gui.ping_info["text"] = ping_text

    def calc_avg_ping(self):
        total = 0

        for curr_tuple in self.runner.ping_data:
            ping_value = curr_tuple[1]
            total = total + ping_value

        avg = total / len(self.runner.ping_data)

        avg_string = "%.f" % avg

        ping_text = "Average Ping: " + avg_string + " ms"

        self.gui.avg_ping["text"] = ping_text

    def update_spikes(self):
        spikes = str(self.runner.lag_spikes)

        self.gui.lag_spikes["text"] = "Number of lag spikes: " + spikes

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

    # update the gui
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
                    self.sql_module.insert_ping_val(self.current_ping_tuple)
                    print(self.sql_module.get_ping_values())

        self.gui.master.after(update_interval, self.check_update_data)
