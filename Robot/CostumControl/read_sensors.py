import socket
import math
from socket import *
import datetime
from typing import AnyStr



class ReadSensors():
    def __init__(self,generalControls) -> None:
        super().__init__()
        self.gc=generalControls
        #sensorDatavariables
        self.sensorValues=dict()
        self.sockFile = self.gc.client_socket.makefile()
        self.MOTDIR = 1
        self.WHEEL_CNT = 380;  #4*5*15/2 = 150 * 1.7 = 255
        self.WHEEL_P = math.pi * 0.27;      #//radius 0.27/2
        self.WHEEL_R = 0.27 / 2
        self.WheelCirc=0.27*math.pi

        self.WHEELDIS = 0.54
        self.estPost = [0,0,0] #/ this is under ENU system, but estPos[2] is orientation, Yaw, not "U"
        self.preEstPos = [0,0,0] #same with estPos
        self.encoderT = 0.2
        # self.defaultTimestamp = 0
        self.afgelegdeAfstand=0
        self.leftDis=0
        self.rightdis=0
        self.index=0
        self.WheelCirc=0.27*math.pi




        
       
        # self.client_socket.setblocking(False)

    def readAll(self):
        #sockFile= self.gc.client_socket.makefile()
        message = self.sockFile.readline().rstrip()
        #print(message)

        try:
            self.process(message)
        except(IndexError,ValueError):
            pass

        return self.sensorValues
           
        
        

       
    
        

    def process(self, message: AnyStr):
        
        if (message.startswith('#')):
            self.process_IMU_message(message)
        elif (message.startswith('MM')):
            self.process_motor_message(message)
        elif (message.startswith('$')):
            pass#self.process_GPS_message(message)

    def process_IMU_message(self, message: AnyStr) -> None:
        # 49,YAW,2.77,GYRO,-3,32,-8,ACC,4,0,252,ADC,1253,400,8,1,
        # print(message)
        strTest = message
        strletter = message.find("W")
        if (strTest[strletter+2] == "-"):
            strprint= strTest[strletter+2] +strTest[strletter+3]+strTest[strletter+4]+strTest[strletter+5] +strTest[strletter+6]
        else:
            strprint= strTest[strletter+2] +strTest[strletter+3]+strTest[strletter+4]+strTest[strletter+5]

        fltprint = float(strprint)
        # print("YAW" + str(fltprint))
        self.sensorValues["IMU"]=message
        self.sensorValues["YAW"]=fltprint

        
        
        #print(message)

    def process_motor_message(self, message: AnyStr) -> None:
        
        """
        :param message: MMX Y=Z   (X = motor driver board id (0=front) or (1=rear) , Y = parameter name, Z = parameter
        (MMX ?Y messages will be ignored)
        """
        driver_board_id = int(message[2])

        if (message[4:].startswith('A=')):
            self.process_motor_current(driver_board_id, message[6:])
        elif (message[4:].startswith('AI=')):
            # digital input
            pass
        elif (message[4:].startswith('C=')):
           
            #print("CCCCC" + str(message[6:]))
            self.process_motor_encoder_position_count(driver_board_id, message[6:])
        elif (message[4:].startswith('D=')):
            # digital input
            pass
        elif (message[4:].startswith('P=')):
            self.process_motor_output_power(driver_board_id, message[6:])
        elif (message[4:].startswith('S=')):
            #pass
            self.process_motor_encoder_velocity(driver_board_id, message[6:])
        elif (message[4:].startswith('T=')):
            self.process_motor_temperature(driver_board_id, message[6:])
        elif (message[4:].startswith('V=')):
            self.process_motor_driver_board_power_voltage(driver_board_id, message[6:])
        elif (message[4:].startswith('CR=')):
            #print("RRRRRRR" + str(message[6:]))
            self.process_motor_encoder_position_count_relative(driver_board_id, message[7:])
        elif (message[4:].startswith('FF=')):
            self.process_motor_driver_board_status(driver_board_id, message[7:])
        else:
            pass
            #print(message)

    def process_GPS_message(self, message: AnyStr) -> None:
        pass
        #print(message)

    def close_connection(self):
       self.gc.close_connection()

    def process_motor_current(self, driver_board_id: int, param: AnyStr) -> None:
        values = param.split(":")
        p = ""
        if driver_board_id == 0:
            p = "Front"
        elif driver_board_id == 1:
            p = "Rear"
        #print("Motor current left {0} = {1}".format(p, values[0]))
        #print("Motor current right {0} = {1}".format(p, values[1]))
        self.sensorValues["MotorCurrentLeft"+p] = values[0]
        self.sensorValues["MotorCurrentRight"+p] = values[1]

    def process_motor_temperature(self, driver_board_id: int, param: AnyStr) -> None:
        values = param.split(":")
        p = ""
        if driver_board_id == 0:
            p = "Front"
        elif driver_board_id == 1:
            p = "Rear"
        #print("Motor temperature left {0} = {1}".format(p, values[0]))
        #print("Motor temperature right {0} = {1}".format(p, values[1]))
        self.sensorValues["MotorTemperatureLeft" +p]=values[0]
        self.sensorValues["MotorTemperatureRight" +p]=values[1]

    def process_motor_encoder_position_count(self, driver_board_id: int, param: AnyStr) -> None:
        values = param.split(":")
        p = ""
        if driver_board_id == 0:
            p = "Front"
           
        elif driver_board_id == 1:
            p = "Rear"
        # print("Encoder position count left {0} = {1}".format(p, values[0]))
        # print("Encoder position count right {0} = {1}".format(p, values[1]))
        
        self.sensorValues["EncoderPositionCountLeft"+p]=values[0]
        self.sensorValues["EncoderPositionCountRight"+p]=values[1]
       

    def process_motor_encoder_position_count_relative(self, driver_board_id: int, param: AnyStr) -> None:
        values = param.split(":")
        p = ""
        if driver_board_id == 0:
            p = "Front"
        elif driver_board_id == 1:
            p = "Rear"
        #print("Encoder position count relative left {0} = {1}".format(p, values[0]))
        #print("Encoder position count relative right {0} = {1}".format(p, values[1]))
        self.sensorValues["EncoderPositionCountRelativeLeft"+p]=values[0]
        self.sensorValues["EncoderPositionCountRelativeRight"+p]=values[1]
        try:
            self.encoderEstimate(values[0],values[1])
        except(KeyError):
            print("pass error")


    def process_motor_output_power(self, driver_board_id: int, param: AnyStr) -> None:
        # motor output power (PWM) -1000~ 1000
        values = param.split(":")
        p = ""
        if driver_board_id == 0:
            p = "Front"
        elif driver_board_id == 1:
            p = "Rear"
        #print("Motor output power left {0} = {1}".format(p, values[0]))
        #print("Motor output power right {0} = {1}".format(p, values[1]))
        self.sensorValues["MotorOutputPowerLeft"+p] = values[0]
        self.sensorValues["MotorOutputPowerRight"+p] = values[1]

    def process_motor_encoder_velocity(self, driver_board_id: int, param: AnyStr) -> None:
        values = param.split(":")
        # newTimeStamp=self.getCurrentTimeInMilliseconds()
        # verschilTimeStamps =  newTimeStamp - self.defaultTimestamp
        # #print("default timestamp" + str(self.defaultTimestamp))
        # self.defaultTimestamp = newTimeStamp
        p = ""
        if driver_board_id == 0:
            p = "Front"
        elif driver_board_id == 1:
            p = "Rear"
        
        #print("Encoder velocity  {0} = {1} RPM".format(p, values[0]))
        #print("Encoder velocity  {0} = {1} RPM".format(p, values[1]))
        #print("value 0" + str(values[0]))
        #print("vershilts" + str(verschilTimeStamps))
        #print("new timestamp" + str(newTimeStamp))
        
        # try:
        #     #print("value die we gebruiken " + str(values[0]))
        #     waarde = float(values[0]) * verschilTimeStamps * (0.27 * math.pi)#0.27METER

        #     #self.afgelegdeAfstand=self.afgelegdeAfstand + waarde
        #     #print("Afgelegde afstand " + str(self.afgelegdeAfstand))
            
        # except(ZeroDivisionError):
        #     waarde=0

        #print ("A??" +  str(waarde))
       
        
        self.sensorValues["EncoderVelocity"+p]=values[0]
        self.sensorValues["EncoderVelocity"+p]=values[1]

    def process_motor_driver_board_power_voltage(self, driver_board_id: int, param: AnyStr) -> None:
        values = param.split(":")
        p = ""
        if driver_board_id == 0:
            p = "Front"
        elif driver_board_id == 1:
            p = "Rear"
        #print("Motor driver board power 12V {0} = {1} V".format(p, int(values[0]) / 10.0))
        #print("Motor driver board power Main {0} = {1} V".format(p, int(values[1]) / 10.0))
        #print("Motor driver board power 5V {0} = {1} V".format(p, int(values[2]) / 1000.0))
        self.sensorValues["MotorDriverBoardPower12V"+p]= int(values[0])/10.00
        self.sensorValues["MotorDriverBoardPowerMain"+p]= int(values[1])/10.00
        # print("VOLT {0}".format(int(values[1])/10.00))
        self.sensorValues["MotorDriverBoardPower5V"+p]= int(values[2])/10.00


    def process_motor_driver_board_status(self, driver_board_id: int, value: AnyStr) -> None:
        
        flags = int(value)
        overheat = flags & 1 > 0
        overvoltage = flags & 2 > 0
        undervoltage = flags & 4 > 0
        short_circuit = flags & 8 > 0
        emergency_stop = flags & 16 > 0
        brushless_sensor_fault  = flags & 32 > 0
        mosfet_failure = flags & 64 > 0
        custom_flag = flags & 64 > 0

        if driver_board_id == 0:
            p = "Front"
        elif driver_board_id == 1:
            p = "Rear"
        #print("Motor driver board status {0} overheat = {1}".format(p, overheat))
        #print("Motor driver board status {0} overvoltage = {1}".format(p, overvoltage))
        #print("Motor driver board status {0} undervoltage = {1}".format(p, undervoltage))
        #print("Motor driver board status {0} short_circuit = {1}".format(p, short_circuit))
        #print("Motor driver board status {0} emergency_stop = {1}".format(p, emergency_stop))
        #print("Motor driver board status {0} brushless_sensor_fault = {1}".format(p, brushless_sensor_fault))
        #print("Motor driver board status {0} mosfet_failure = {1}".format(p, mosfet_failure))
        #print("Motor driver board status {0} custom_flag = {1}".format(p, custom_flag))
        self.sensorValues["MotorDriverBoardStatusOverheat"+p] = overheat
        self.sensorValues["MotorDriverBoardStatusOverVoltage" +p] = overvoltage
        self.sensorValues["MotorDriverBoardStatusUnderVoltage" +p] = undervoltage
        self.sensorValues["MotorDriverBoardStatusShortCircuit" +p] =short_circuit
        self.sensorValues["MotorDriverBoardStatusEmergencyStop" +p] =emergency_stop
        self.sensorValues["MotorDriverBoardStatusBrushlessSensorFault" +p] =brushless_sensor_fault
        self.sensorValues["MotorDriverBoardStatusMostfetFailure" +p] =mosfet_failure
        self.sensorValues["MotorDriverBoardStatusCostumFlag" +p] = custom_flag

    # def calculateDistance(LeftFrontencoderAbs,leftBackEncoderAbs,RightFrontencoderAbs,RightBackEncoderAbs):
    #     # self.sensorValues["EncoderPositionCountLeft"+p]=values[0]
    #     # self.sensorValues["EncoderPositionCountRight"+p]=values[1]
        
    #     leftDifferenceFront=int(LeftFrontencoderAbs)-int(leftFrontEncoderStart)
    #     leftDifferenceBack=int(leftBackEncoderAbs)*int(leftBackEncoderStart)

    #     RightDifferenceFront=int(RightFrontencoderAbs)-int(RightFrontencoderStart)
    #     RightDifferenceBack=int(RightBackEncoderAbs)*int(RightBackEncoderStart)

        
    #     leftDistanceTravelled=((leftDifferenceFront+leftDifferenceBack) /2)  * WheelCirc /380
    #     RightDistanceTravelled =((RightDifferenceFront+RightDifferenceBack)/2)  *WheelCirc /380

    #     print("LEFT" + str(leftDistanceTravelled))
    #     print("RIGHT" + str(RightDistanceTravelled))
    
    def encoderEstimate(self,leftEncoder,rightEncoder):
        leftDis=self.leftDis
        rightDis = self.rightdis
        firstEncoder=False
        leftEncoder=float(leftEncoder)
        rightEncoder=float(rightEncoder)
        # print("LEFTENCONDER " + str(leftEncoder))
        
       

       
        leftDis= self.MOTDIR * leftEncoder / self.WHEEL_CNT * (2 * math.pi * self.WHEEL_R)
            
            
        rightDis = -self.MOTDIR * rightEncoder / self.WHEEL_CNT * (2 * math.pi * self.WHEEL_R)
            
        vel = (leftDis + rightDis) / 2 / self.encoderT
        self.sensorValues["vel"]=vel   
            
        self.rightdis=self.rightdis+rightDis
        self.leftDis=self.leftDis + leftDis
        # print("leftDisInFunction " + str(self.leftDis))
        #print("RightDisInFunction " + str(self.rightdis))
        self.sensorValues["leftDis"]=self.leftDis
        self.sensorValues["rightDis"]=self.rightdis

    

        

             
    def getCurrentTimeInMilliseconds(self):
        #test = time.time()
        #print("TEST" + str(test))
        now=datetime.datetime.now()

        
        milliseconds = now.minute
        #float(time.time() * 1000.0)
        return milliseconds


            

        


       






