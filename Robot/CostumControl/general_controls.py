import socket
import time
from socket import *
from Robot_config import *

class GeneralControls:
    send_freq: int = 5  # Hz
    
    def __init__(self) -> None:
        super().__init__()
        self.client_socket: socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
        self.client_socket.connect((RobotIP, Port1))

    def ping(self) -> None:
        self.send_cmd("PING")

    def send_cmd(self, cmd: str) -> None:
        data = bytes(cmd, 'utf-8') + b'\r\n'
        # data_send: int = self.client_socket.send(data)
        # if data_send != len(data):
        #     raise RuntimeError
        self.client_socket.sendall(data)
        if (cmd != "PING"):
            print(cmd)
        
        # time.sleep(1.0/self.send_freq)

    def close_connection(self):
        self.client_socket.close()

