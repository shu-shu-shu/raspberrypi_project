# -*- coding: utf-8 -*-

import smbus
from time import sleep

# SHT31D Registers
bus = smbus.SMBus(1) # 1 = /dev/i2c-1 (port I2C1) �m�F�ς�
address_SHT31 = 0x45 #i2c address
reg_1mps_read_MSB = 0x21
reg_1mps_read_LSB = 0x26
reg_start_seq_read_MSB = 0xe0
reg_start_seq_read_LSB = 0x00

one_minutes = 60
one_hours = 60 * one_minutes
loop = 5


#�����x�Z���TSHT31�̘A���ǂݍ��� i2c write
def init_SHT31():
    bus.write_byte_data(address_SHT31, reg_1mps_read_MSB, reg_1mps_read_LSB)
    sleep(0.1)
    print("success")

#�����x�Z���TSHT31�̘A���ǂݍ��� i2c read
def read_SHT31():
	#�A���ǂݍ��݊J�n�@i2c write
    bus.write_byte_data(address_SHT31, reg_start_seq_read_MSB, reg_start_seq_read_LSB)
    sleep(0.1)
    #�A���ǂݍ��ݎ�M
    block_data = bus.read_i2c_block_data(address_SHT31, 0) #�������͕K�v���Ȃ������Ɋ֐����Ȃ��̂�0�}��
    temperature = -45.0 + (175.0 * ((block_data[0] * 256) + block_data[1]) / 65535.0) #�ێ�
    humidity = (100.0 * ((block_data[3] * 256.0) + block_data[4])) / 65535.0
    print("temperature:", temperature)
    print("humidity", humidity)
    return {'temperature':temperature, 'humidity':humidity}

#tension�f�[�^�ւ̕ϊ��A���̊֐����g���O��init_SHT31()������K�v����
def get_tension():
    pre_raw_data = read_SHT31()
    sleep(one_minutes)
    for i in range(loop):
        raw_data = read_SHT31()
        difference = raw_data["humidity"] - pre_raw_data["humidity"]
        tension = (difference / 2) + 50 #50�𒆐S�Ƃ���0~100�̒l��
        print("tension", tension)
        pre_raw_data = raw_data
        sleep(one_minutes)
    return(tension)
