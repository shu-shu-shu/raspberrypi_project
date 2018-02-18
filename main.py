# -*- coding: utf-8 -*-



from time import sleep
import datetime
import requests
import json
import sht31d
import getPulse


url = 'http://xxx.xx.xxx.xxx:5000'
one_minutes = 60
one_hours = 60 * one_minutes
one_day = 24 * one_hours

loop = one_day

def main():
    sht31d.init_SHT31()
    sht_pre_raw_data = sht31d.read_SHT31()
#    getPulse.open_serial()
    sleep(1)
    for i in range(loop):

        sht_raw_data = sht31d.read_SHT31()
        difference = sht_raw_data["humidity"] - sht_pre_raw_data["humidity"]
        tension = (difference / 4) + 25 #1~50の値の範囲に調整
        print("tension", tension)
        sht_pre_raw_data = sht_raw_data
#        getPulse_result = getPulse.get_pulse()
        t = datetime.datetime.now()

        json_tension = json.dumps({'ID':'xxx','sensor_name':'tension', 'timestamp':'%s'%t.strftime("%Y-%m-%d %H:%M:%S"), 'data_float':'%s'%tension})
        json_temperature = json.dumps({'ID':'xxx','sensor_name':'SHT31_temperature', 'timestamp':'%s'%t.strftime("%Y-%m-%d %H:%M:%S"), 'data_float':'%s'%(sht_raw_data["temperature"])})
        json_humidity = json.dumps({'ID':'xxx','sensor_name':'SHT31_humidity', 'timestamp':'%s'%t.strftime("%Y-%m-%d %H:%M:%S"), 'data_float':'%s'%(sht_raw_data["humidity"])})
#        json_pulse = json.dumps({'ID':'xxx','sensor_name':'pulse', 'timestamp':'%s'%t.strftime("%Y-%m-%d %H:%M:%S"), 'data_float':'%s'%getPulse_result})

        #http post���M
        r = requests.post(url, json_tension)
        print(r.status_code)
        r = requests.post(url, json_temperature)
        print(r.status_code)
        r = requests.post(url, json_humidity)
        print(r.status_code)

#        r = requests.post(url, json_pulse)
#        print(r.status_code)
#        if not getPulse_result == -1:
#            r = requests.post(url, json_pulse)
#            print(r.status_code)

        sleep(one_minutes)

    getPulse.close_serial()
    return

if __name__ == "__main__":
    main()
