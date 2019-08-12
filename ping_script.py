import subprocess
import time
import threading
import platform
from timeit import default_timer


# class used to call ping on different OS platforms
class PingRunner:

    def __init__(self):
        self.ping_data = []
        self.lag_spikes = 0
        self.process = None
        self.stop_thread = False
        self.found_index = None
        self.data_changed = False
        self.start_time = None

    # used to get the time data from the line created by the terminal
    def parse_line(self, ping_line):
        words = ping_line.split()
        for word in words:

            ping_substring = "time="

            if ping_substring in word:
                if self.found_index is None:
                    self.found_index = PingRunner.find_end_index(word)
                    
                if self.found_index == 0:
                    ping_time = word[len(ping_substring):]
                else:
                    ping_time = word[len(ping_substring):self.found_index]
                    
                ping_time = float(ping_time)
                return ping_time

    # utility method for parse_line
    @staticmethod
    def find_end_index(word):
        end_index = 0
        for test_char in reversed(word):
            if str.isdigit(test_char):
                return end_index
            end_index -= 1

    # pings Riot's ip's to test for lag
    def run_ping_test(self, server):
        self.init_runner()

        if platform.system() == "Windows":
            self.process = subprocess.Popen(["ping", "-t", server], shell=False,
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Unix and Mac
        else:
            self.process = subprocess.Popen(["ping", server], shell=False,
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.process.stdout.readline()
        self.process.stdout.readline()

        while True:
            if self.stop_thread:
                # print("Calling stop_ping_test!")
                self.stop_ping_test()

            line = self.process.stdout.readline()
            if line:
                decoded_line = line.decode("utf-8")

                # for debugging purposes
                # print(decoded_line)

                data_parsed = self.parse_line(decoded_line)

                self.handle_data(data_parsed)

                # setting dirty bit to true
                self.data_changed = True
            else:
                break

    def handle_data(self, data):
        # occurs if ping request is timed out
        if data is None:
            self.lag_spikes += 1
        else:
            if self.start_time is None:
                self.start_time = default_timer()
                current_time = self.start_time
            else:
                current_time = default_timer()

            # rounding time_elapsed to integer
            time_elapsed = int(round(current_time - self.start_time))
            ping_tuple = (time_elapsed, data)
            self.ping_data.append(ping_tuple)

    # signals for process to stop
    def stop_ping_test(self):
        self.process.terminate()

    # reinitialize runner to default values
    def init_runner(self):
        self.ping_data = []
        self.lag_spikes = 0
        self.process = None
        self.stop_thread = False
        self.start_time = None

    def show_ping_data(self):
        print(self.ping_data)


# Used for testing
if __name__ == "__main__":
    na_server = "104.160.131.3"

    runner = PingRunner()

    thread1 = threading.Thread(target=runner.run_ping_test, args=(na_server,))
    # thread1.daemon = True
    thread1.start()

    time.sleep(5)

    runner.stop_thread = True

    time.sleep(5)


