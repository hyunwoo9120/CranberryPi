import cv2
from datetime import datetime
import threading
import time
import boto3

cam = cv2.VideoCapture(0,cv2.CAP_V4L)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height
#config
s3=boto3.client('s3',
   aws_access_key_id='access_key',
   aws_secret_access_key='secret_access_key')

def print_real():
    ret, img =cam.read()
    now =datetime.now()
    realti=str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
    filename1='image/'+realti+'.jpg'
    filename2=realti+'.jpg'
    cv2.imwrite("image/"+realti+".jpg",img)

    bucket_name='bucket_name'
    s3.upload_file(filename1,bucket_name,filename2)
    threading.Timer(0.5,print_real).start()

print_real()
