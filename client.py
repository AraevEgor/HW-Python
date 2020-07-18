import psutil
import socket
# import threading
from time import sleep


# Откровенно говоря запутался с классом-сборщиком и тем, как управлять им через threading

# class DataCollector:
#     def __init__(self, metric):
#         self.metric = metric
#         self.value = None
#         self.collect = True
#
#     def start_collect(self):
#         while self.collect:
#             if self.metric == 'cpu_usage':
#                 self.value = psutil.cpu_percent(interval=1)
#
#     def get_current_state(self):
#         return self.value
#
#     def cleanup(self):
#         self.value = None
#
#     def stop_collect(self):
#         self.collect = False


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 9999))
        # dc = DataCollector('cpu_usage')
        # threading.Thread(target=dc.start_collect())
        counter = 0
        while True:
            # counter += 1
            # if counter > 5:    # stop collecting the data after 5 iterations
            #     dc.stop_collect()
            #     dc.cleanup()
            s.send(f'CPU usage: {psutil.cpu_percent()}'.encode('utf-8'))
            sleep(60)
