import subprocess


# class used to call ping in Command Prompt on Windows
class PingRunner:

    def __init__(self):
        self.ping_data = []
        self.lag_spikes = 0

    def parse_line(self, ping_line):
        words = ping_line.split()
        for word in words:

            ping_substring = "time="

            if ping_substring in word:
                ping_time = int(word[len(ping_substring):-2])
                return ping_time

    # pings Riot's ip's to test for lag
    def run_ping_test(self, server):

        p = subprocess.Popen(["ping", "-t", server], shell=False,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.stdout.readline()
        p.stdout.readline()
        while True:
            line = p.stdout.readline()
            if line:
                decoded_line = line.decode("utf-8")
                print(decoded_line)
                data_parsed = self.parse_line(decoded_line)
                # occurs if ping request is timed out
                if data_parsed is None:
                    self.lag_spikes += 1
                else:
                    self.ping_data.append(data_parsed)
            else:
                break


if __name__ == "__main__":
    na_server = "104.160.131.3"

    runner = PingRunner()

    runner.run_ping_test()

