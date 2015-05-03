# -*- coding: utf-8 -*
"""
Created 20150102

@author: G. Kettlewell

Read in data from serial port send by the Arduino adn plot it using a live update.
"""

import datetime as dt
import serial
import matplotlib.pyplot as plt
#import numpy as np
#from pylab import pause
from drawnow import *

def updatePlot():
    plt.ylim(-5,35)
    plt.title("Sensor data")
    plt.grid(True)
    plt.ylabel("Temp C")
    plt.plot(temperature1, 'r-', label='Ambient' + ': ' + '        ' 
        + str(temperature1[len(temperature1) -1]) + 'C')
    plt.plot(temperature2, 'g-', label='Camera' + ': ' + '         ' 
        + str(temperature2[len(temperature1) -1]) + 'C')
    plt.plot(temperature3, 'b-', label='Cold plate' + ': ' + '     ' 
        + str(temperature3[len(temperature1) -1]) + 'C')
    plt.plot(temperature4, 'k-', label= 'Dehumidifier' + ': ' + ' ' 
        + str(temperature4[len(temperature1) -1]) + 'C')
    plt.plot(temperature5, 'c-', label='Heatsink' + ': ' + '        ' 
        + str(temperature5[len(temperature1) -1]) + 'C')
    #plt.plot(temperature6, 'b-', label='LM335 5' + ': ' + str(temperature6[len(temperature1) -1]) + 'C')
    plt.plot(dewPoint, 'm-', label='Dew Point' + ': ' + '      '
        + str(dewPoint[len(dewPoint) -1]) + 'C')
    leg = plt.legend(loc='lower left',ncol=1, fancybox = True)
    leg.get_frame().set_alpha(0.5)
    plt2 = plt.twinx()
    plt2.set_ylabel("Relative Humidity")
    #t0 = date[0] - dt.timedelta(0,300)
    #t1= date[len(date) -1 ] + dt.timedelta(0,300)
    #plt.xlim(t0,t1)
    plt.xlim(0,600)
    plt.ylim(0, 100)
    plt2.plot(humidity, 'y-', label='Humidity ' + ': ' + str(humidity[len(humidity) -1]) + '%')
    leg = plt2.legend(loc='lower right',ncol=1, fancybox = True)
    leg.get_frame().set_alpha(0.5)
    plt.draw

ser = serial.Serial('COM18', 9600, timeout=1)

date = []
temperature1 = []
temperature2 = []
temperature3 = []
temperature4 = []
temperature5 = []
temperature6 = []
humidity = []
dewPoint = []

plt.ion()

while True:
    while (ser.inWaiting == 0):
        dt.pause(0.5)

    read_val = ser.readline()
    ser.flushInput()
    pos = read_val.find('Fail')
    if (pos == -1):
        readOK = True
    else:
        readOK = False
    #print readOK
    if (read_val != '' and readOK):
        #date = dt.datetime.now()
        vals = read_val.split(',')
        humidity.append(float(vals[0]))
        temperature1.append(float(vals[1]))
        temperature2.append(float(vals[2]))
        temperature3.append(float(vals[3]))
        temperature4.append(float(vals[4]))
        temperature5.append(float(vals[5]))
        temperature6.append(float(vals[6]))
        dewPoint.append(int(vals[7]))
        if (len(humidity) > 600):
            #date.pop(0)
            humidity.pop(0)
            temperature1.pop(0)
            temperature2.pop(0)
            temperature3.pop(0)
            temperature4.pop(0)
            temperature5.pop(0)
            temperature6.pop(0)
            dewPoint.pop(0)

        drawnow(updatePlot)
        plt.pause(0.001)
    else:
        if (read_val == ''):
            pass
            #print 'Empty string read in'
        else:
            print 'Error reading DHT'

ser.close()
