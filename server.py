from datetime import datetime
import socket

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('localhost', 9999))
        s.listen()
        while True:
            client, addr = s.accept()
            print('Connected by', addr)
            with client:
                while True:
                    data = client.recv(1024)
                    if not data:
                        break
                    decoded = data.decode('utf-8')
                    time = datetime.now().isoformat(sep=' ', timespec='seconds')
                    res = f'{time}:\n {decoded}\n'
                    with open('results.txt', 'a') as f:
                        f.write(res)
