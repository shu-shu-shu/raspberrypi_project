#!/usr/bin/env python coding:utf-8
# -*- coding: utf-8 -*-

import serial
import time

def open_serial():
    #シリアル開始
    global ser
    ser = serial.Serial("/dev/ttyACM0",baudrate=9600,timeout=5)
    time.sleep(10)

def get_pulse():

    #センサ値読み込み
    pulse = ser.readline()
    pulse = pulse.strip()
#   if pulse < 1 or pulse > 200:
#       pulse = -1
#       print("not pulse")
#   else:
#        print("pulse", pulse)
    print("pulse", pulse)
    return pulse

def close_serial():
    ser.close()

