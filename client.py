import psutil
import socket
import threading
from time import sleep


class DataCollector(threading.Thread):
    def __init__(self, metric):
        super().__init__()
        self.metric = metric
        self.value = None
        self.collect = None

    def start_collect(self):
        self.collect = True
        self.start()

    def run(self):
        while self.collect:
            if self.metric == 'cpu_usage':
                self.value = psutil.cpu_percent(interval=1)

    def get_current_state(self):
        return self.metric, self.value

    def cleanup(self):
        self.value = None

    def stop_collect(self):
        self.collect = False


if __name__ == '__main__':
    dc = DataCollector('cpu_usage')
    dc.start_collect()
    counter = 0
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', 9999))
                counter += 1
                res = dc.get_current_state()
                s.send(f'{res[0]}, {res[1]}'.encode('utf-8'))
                if counter == 6:    # stop collecting the data after 5 iterations
                    dc.stop_collect()
                    dc.cleanup()
            sleep(10)
        except:
            break
