# -*- coding: utf-8 -*-

import smbus
from time import sleep
import socket
import datetime
import json
host = "xxx.xxx.xxx" #local
port = xxx #tcp

# SHT31D Registers
bus = smbus.SMBus(1) # 1 = /dev/i2c-1 (port I2C1) 確認済み
address_SHT31 = 0x45 #i2c address
reg_1mps_read_MSB = 0x21
reg_1mps_read_LSB = 0x26
reg_start_seq_read_MSB = 0xe0
reg_start_seq_read_LSB = 0x00
one_minutes = 60
one_hours = 60 * one_minutes

#温湿度センサSHT31の連続読み込み i2c write
def init_seq_read_SHT31():
    bus.write_byte_data(address_SHT31, reg_1mps_read_MSB, reg_1mps_read_LSB)
    sleep(0.1)
    print("success")

#温湿度センサSHT31の連続読み込み i2c read
def read_SHT31():
	#連続読み込み開始　i2c write
    bus.write_byte_data(address_SHT31, reg_start_seq_read_MSB, reg_start_seq_read_LSB)
    sleep(0.1)
    #連続読み込み受信
    block_data = bus.read_i2c_block_data(address_SHT31, 0) #第二引数は必要がないが他に関数がないので0挿入
    temperature = -45.0 + (175.0 * ((block_data[0] * 256) + block_data[1]) / 65535.0) #摂氏
    humidity = (100.0 * ((block_data[3] * 256.0) + block_data[4])) / 65535.0
    print("temperature:", temperature)
    print("humidity", humidity)
    return {'temperature':temperature, 'humidity':humidity}

def main():
    init_seq_read_SHT31()
    for i in range(5):
        result = read_SHT31()
        t = datetime.datetime.now()
        json_temperature = json.dumps({'sensor_name':'SHT31_temperature', 'timestamp':'%s'%t.strftime("%Y-%m-%d %H:%M:%S"), 'data_float':'%s'%(result["temperature"])})
        json_humidity = json.dumps({'sensor_name':'SHT31_humidity', 'timestamp':'%s'%t.strftime("%Y-%m-%d %H:%M:%S"), 'data_float':'%s'%(result["humidity"])})
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #オブジェクトの作成をします
        client.connect((host, port)) #これでサーバーに接続します
        #client.send("temperature:", result['temperature'], "humidity:", result['humidity']) #適当なデータを送信します（届く側にわかるように
        client.send(json_temperature)
        response = client.recv(4096) #レシーブは適当な2の累乗（大きすぎるとダメ）
        print response

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #オブジェクトの作成をします
        client.connect((host, port)) #これでサーバーに接続します
        client.send(json_humidity)
        response = client.recv(4096) #レシーブは適当な2の累乗（大きすぎるとダメ）
        print response
        sleep(one_minutes)
    return

if __name__ == "__main__":
    main()
