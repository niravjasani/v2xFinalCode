'''
    File Name: gps.py
    Description: By enabling serial port ttyS0 with 9600 baud rate, it takes all gps frame that are comming 
                 from the UBlox 6M module.
                 From all the frame getLocation method of this class will filter only "$GNGLL" frame and using pynmea2 module.
                 Finally, returns the current latitude and longitude.
    Author:      Nirav Jasani 
    Date:        Version 1.0(February 3 -2020):
                    Working successfully with UBlox 6M
'''

import serial,time,string,pynmea2

class Gps:

    port="/dev/ttyS0" #defining port
    sr=serial.Serial(port,baudrate=9600,timeout=1)#initiating serial port with desired baudrate and timeout time

    def __init__(self):
        pass

    def getLocation(self):
        self.dout=pynmea2.NMEAStreamReader() #stores the frames into self.dout
        self.newData=Gps.sr.readline().decode()
        '''
            Filtering the $GNGLL frame
        '''
        if self.newData[0:6]=="$GNGLL":
            self.newMsg=pynmea2.parse(self.newData)
            self.lat=self.newMsg.latitude
            self.lng=self.newMsg.longitude
            self.gps=str(self.lat) + " , " + str(self.lng)
            return (self.lat,self.lng)

