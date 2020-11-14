import os
import sys
from argparse import ArgumentParser
import subprocess
import time
from datetime import datetime
import Adafruit_DHT as dht
import requests
import cv2
import numpy as np
import threading
import boto3

TOKEN=""
DEVICE_LABEL="Control_AC"
VARIABLE_LABEL_1="indoor_temp"
VARIABLE_LABEL_2="setting_temp"
VARIABLE_LABEL_3="person_num"
VARIABLE_LABEL_4="power"

onoff = "python3 irrp.py -p -g22 -fhome_aircon power"
up = "python3 irrp.py -p -g22 -fhome_aircon upTemperature"
down = "python3 irrp.py -p -g22 -fhome_aircon downTemperature"

st=0

s3 = boto3.client('s3',
    aws_access_key_id='',
    aws_secret_access_key='')

#cam = cv2.VideoCapture(0,cv2.CAP_V4L)
#cam.set(3, 640) # set video widht
#cam.set(4, 480) # set video height

arr = ""
myfile = ""

def build_payload(variable1,variable2,variable3,variable4):
    payload = {variable1:temperature, variable2:temperature, variable3:person_num, variable4:power}
    return payload
    
def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

def print_real():
    cam=cv2.VideoCapture(0,cv2.CAP_V4L)
    cam.set(3, 640)
    cam.set(4, 480)
    ret, img = cam.read()
    now = datetime.now()
    realti = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
    filename1 ='image/'+realti+'.jpg'
    filename2 =realti+'.jpg'
    cv2.imwrite("image/"+realti+".jpg",img)

    bucket_name=''
    s3.upload_file(filename1,bucket_name,filename2)

def gpn():
    for object in s3.list_objects(Bucket='')['Contents']:
        s3.download_file('', object['Key'], object['Key'])
        arr=object['Key']
    myfile=open(arr,'r',encoding='utf-8')
    mystring=myfile.read()

    return int(mystring) 

def check_hour():
    now = datetime.now()
    return now.hour

def check_month():
    now = datetime.now()
    month = int(now.month)
    if(month==11 or month==12
        or month==1 or month==2):
        return 'cool'
    if(month==5 or month==6
        or month==7 or month==8):
        return 'cool'
    else:
        return 'default'

def check_temp():
    _,it = dht.read_retry(dht.DHT11,14)
    return it

def set_temp(tmp):
    global st
    print('check st: {0}, check tmp: {1}'.format(st, tmp))
    if(st<tmp):
        for i in range(tmp-st+1):
            time.sleep(1)
            if(os.system(up) != 0):
                print('up error')
                break
        st=tmp
    elif(tmp<st):
        for i in range(st-tmp+1):
            time.sleep(1)
            if(os.system(down) != 0):
                print('down error')
                break
        st=tmp
    print('setted st: {0}'.format(st))

#pn : person num
#it : indoor temp
#st : setted temp
#s : state
#sys : cool or heat
'''starting off'''

def main(init_temp):
    sys=check_month()
    s=0 #off
    global st
    st=int(init_temp)
    if(sys=='cool'):
        print('Start Cooling Control!')
        print('======================')
        while True:
            it=check_temp()
            print("indoor temperature: {0}".format(it))
            hour=check_hour()
            print("hour: {0}".format(hour))
            '''
            if(hour==12 or hour==17):
                if(s==1):
                    if(os.system(onoff) != 0):
                        print('onoff error')
                        break
                    print('off')
                print('time to off!')
                continue
            '''
            print_real()
            time.sleep(3)
            pn=gpn()
            print("num of people: {0}".format(pn))
            #time.sleep(2)
            if(s==1 and (it<22 or pn==0)):
                if(os.system(onoff) != 0):
                    print('onoff error')
                    break
                print('off')
                s=0
            else:
                #if(it<=26):
                #    continue
                if(it==22 and 0<pn):
                    if(s==0):
                        if(os.system(onoff) != 0): 
                            print('onoff error')
                            break
                        print('on')
                        s=1
                        time.sleep(7)
                    if(0<pn<=1):
                        set_temp(24)
                    if(1<pn<=2):
                        set_temp(23)
                    if(2<pn<=3):
                        set_temp(22)
                    print("setting_temperature: {0}".format(st))
                elif(it==23 and 0<pn):
                    if(s==0):
                        if(os.system(onoff) != 0): 
                            print('onoff error')
                            break
                        print('on')
                        s=1
                        time.sleep(7)
                    if(0<pn<=1):
                        set_temp(24)
                    if(1<pn<=2):
                        set_temp(23)
                    if(2<pn<=3):
                        set_temp(22)
                    print("setting_temperature: {0}".format(st))
                elif(it>=24 and 0<pn):
                    if(s==0):
                        if(os.system(onoff) != 0):
                            print('onoff error')
                            break
                        print('on')
                        s=1
                        time.sleep(7)
                    if(0<pn<=1):
                        set_temp(24)
                    if(1<pn<=2):
                        set_temp(23)
                    if(2<pn<=3):
                        set_temp(22)
                    print("setting_temperature: {0}".format(st))

                else:
                    continue
            #--------ubidots---------
            payload = {VARIABLE_LABEL_1:it,VARIABLE_LABEL_2:st,VARIABLE_LABEL_3:pn,VARIABLE_LABEL_4:s}
            post_request(payload)
            print("[INFO] send to ubidots")
            #------------------------

    if(sys=='heat'):
        print('Start Heating Control!')
        print('======================')
        while True:
            hour=check_hour()
            if(hour=='12' or hour=='17'):
                continue
            print_real()
            time.sleep(3)
            pn=gpn()
            time.sleep(2)
            check_temp()
            if(s==1 and (it>20 or pn==0)):
                if(os.system(onoff) != 0):
                    print('onoff error')
                    break
                print('off')
                s=0
            else:
                if(it>=18):
                    continue
                if(s==0 and (it==20 and pn<=10)):
                    if(os.system(onoff) != 0):
                        print('onoff error')
                        break
                    print('on')
                    s=1
                    set_temp(20)
                elif(s==0 and (it==19 and pn<=20)):
                    if(os.system(onoff) != 0):
                        print('onoff error')
                        break
                    print('on')
                    s=1
                    if(0<pn<=10):
                        set_temp(20)
                        print("setting_temperature: {0}".format(st))
                    if(10<pn<=20):
                        set_temp(19)
                elif(s==0 and (it<=18)):
                    if(os.system(onoff) != 0):
                        print('onoff error')
                        break
                    print('on')
                    s=1
                    if(0<pn<=10):
                        set_temp(20)
                    if(10<pn<=20):
                        set_temp(19)
                    if(20<pn<=30):
                        set_temp(18)
                else:
                    continue
    else:
        print("There's no need for cooling and heating!")
    
if __name__=='__main__':
    parser = ArgumentParser(description='control Air Conditioner')
    parser.add_argument("--input_initial_temp",help=" ")
    args=parser.parse_args()
    input_initial_temp=args.input_initial_temp
    main(input_initial_temp)

