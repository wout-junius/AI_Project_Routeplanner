import socket
import time
import threading
from socket import *
from Robot_config import *
from general_controls import GeneralControls
from read_sensors import ReadSensors


class Controls:
    send_freq: int = 5  # Hz

    def __init__(self) -> None:
        super().__init__()
        self.generalControls=GeneralControls()
        self.readSensors=ReadSensors(self.generalControls)
        

    def constantping(self):
        self.generalControls.ping()

       

    
    def stop(self) -> None:
        self.generalControls.send_cmd("MMW !M 0 0")
        print("stopped")
       

    def go_forward(self,power: int, seconds: int) -> None:
        self.generalControls.send_cmd("MMW !M {0} -{1}".format(str(power), str(power)))
        
        
    
    def go_backward(self, power: int, seconds: int) -> None:
        self.generalControls.send_cmd("MMW !M -{0} {1}".format(str(power), str(power)))
        # self.stop()

    def turn_left(self, power: int, seconds: int) -> None:
        self.generalControls.send_cmd("MMW !M -{0} -{1}".format(str(power), str(power)))
        # for i in range(0, seconds * self.send_freq):
        #     self.generalControls.ping()
        # self.stop()

    def turn_right(self,power: int, seconds: int) -> None:
        self.generalControls.send_cmd("MMW !M {0} {1}".format(str(power), str(power)))
        
   
    def emergency_stop(self) -> None:
        self.generalControls.send_cmd("MMW !M 0 0")
        self.generalControls.send_cmd("MMW !EX")

    def emergency_stop_release(self) -> None:
        self.generalControls.send_cmd("EGPS 0")
        self.generalControls.send_cmd("MMW !MG")

    def close_connection(self)->None:
        
        self.generalControls.close_connection()
    

    

