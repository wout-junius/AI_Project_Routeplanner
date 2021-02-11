import logging
from threading import Thread
from queue import Queue 
from time import time, sleep
import time
import atexit
import threading
import math
import sys
import json
import requests
from move_controls import Controls
from general_controls import GeneralControls
from datetime import datetime


JsonFileName="jsonData.json"
lastPositionFile="LastPos.txt"

commandArray=[]


class ApiControls():
    def __init__(self):
        super().__init__()

    def WritePositionToTextfile(self,lastPos):
        with open(lastPositionFile,'w') as text_file:
            text_file.write(str(lastPositionFile))


    def readLastCommandIdFromFile(self):
        with open(lastPositionFile) as text_file:
            dataLastCmdId= text_file.read()
        return lastPositionFile



    def getNextMove(self):
        url="http://127.0.0.1:3000/getmoves"
        x=requests.get(url)
        print(x)
        data=x.json()
        print(data)
        # writeToJsonFile(data)
        for ele in data:
            if "Empty" in ele.keys():
                return False
        return data


    def writeToJsonFile(self,data):
        with open(JsonFileName, 'w') as json_file:
            json.dump(data, json_file)

    def ReadFromJsonFile(self):
        with open(JsonFileName) as json_file:
            data = json.load(json_file)
        # print (data)
        return data

    def getAllMoves(self):
        data=self.getNextMove()
        while data == False:
            data=self.getNextMove()
        self.writeToJsonFile(data)
        return 1

# if __name__ == "__main__":
#     getAllMoves()
#     ReadFromJsonFile()
#     print("DONE")
    

