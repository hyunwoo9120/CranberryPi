import os
import subprocess
import time
import threading

it = 0 #it : indoor temp
pn = 0 #pn : person num

up = "python3 irrp.py -p -g23 -fairconup"
down = "python3 irrp.py -p -g23 -faircondown"
onoff = "python3 irrp.py -p -g23 -fairconpower"
#indoor_temp = "python3 humidtest.py"

def switch(x):
    return({11,12,1,2:'heat', 5,6,7,8:'cool'}.get(x,'default'))

def check_temp():
    it=subprocess.check_output(['python3','temperature.py'])
    threading.Timer(300,check_temp).start() '''5min'''

def check_pn():
    #it=subprocess.check_output(['python3','humidtest.py'])
    threading.Timer(300,check_temp).start() '''5min'''

def set_temp(st,tmp):
    if(st<tmp):
        while(st==tmp):
            if(os.system(up) != 0): '''up'''
                print('up error')
                break
            st++
    if(tmp<st):
        while(st==tmp):
            if(os.system(down) != 0): '''down'''
                print('down error')
                break
            st--

#pn : person num
#it : indoor temp
#st : setted temp
#s : state
#sys : cool or heat
'''starting off'''
def main(month, init_temp):
    sys=switch(month)
    s=0 #off
    st=init_temp
    check_temp()
    #check_pn()
    if(sys=='cool'):
        print('Start Cooling Control!')
        print('======================')
        while True:
            sleep
            if(s==1 and (it<24 or pn==0)):
                if(os.system(onoff) != 0): '''off'''
                    print('onoff error')
                    break
                s=0
            else:    
                if(it<=26): '''꺼져있을 때 는 처음상황에서는 26도 보다 크면 on'''
                    continue                
                if(s==0 and (it==24 and 20<pn)):
                    if(os.system(onoff) != 0): '''on'''
                        print('onoff error')
                        break
                    s=1
                    '''set temp 24'''
                    set_temp(st,24)
                else if(s==0 and (it==25 and 10<pn)):
                    if(os.system(onoff) != 0): '''on'''
                        print('onoff error')
                        break
                    s=1
                    if(10<pn<=20):
                        '''set temp 25'''
                        set_temp(st,25)
                    if(20<pn<=30):
                        '''set temp 24'''
                        set_temp(st,24)
                else if(s==0 and (it>=26)):
                    if(os.system(onoff) != 0): '''on'''
                        print('onoff error')
                        break
                    s=1
                    if(0<pn<=10):
                        '''set temp 26'''
                        set_temp(st,26)
                    if(10<pn<=20):
                        '''set temp 25'''
                        set_temp(st,25)
                    if(20<pn<=30):
                        '''set temp 24'''
                        set_temp(st,24) 
                else:
                    continue
            
    if(sys=='heat'):
        print('Start Heating Control!')
        print('======================')
        while True:
            if(s==1 and (it>20 or pn==0)):
                if(os.system(onoff) != 0): '''off'''
                    print('onoff error')
                    break
                s=0
            else:    
                if(it>=18): '''꺼져있을 때 켜는 처음상황에서는 18도 보다 작으면 on'''
                    continue
                if(s==0 and (it==20 and pn<=10)):
                    if(os.system(onoff) != 0): '''on'''
                        print('onoff error')
                        break
                    s=1
                    '''set temp 20'''
                    set_temp(st,20)
                else if(s==0 and (it==19 and pn<=20)):
                    if(os.system(onoff) != 0): '''on'''
                        print('onoff error')
                        break
                    s=1
                    if(0<pn<=10):
                        '''set temp 20'''
                        set_temp(st,20)
                    if(10<pn<=20):
                        '''set temp 19'''
                        set_temp(st,19)
                else if(s==0 and (it<=18)):
                    if(os.system(onoff) != 0): '''on'''
                        print('onoff error')
                        break
                    s=1
                    if(0<pn<=10):
                        '''set temp 20'''
                        set_temp(st,20)
                    if(10<pn<=20):
                        '''set temp 19'''
                        set_temp(st,19)
                    if(20<pn<=30):
                        '''set temp 18'''
                        set_temp(st,18) 
                else:
                    continue
            
    else:
        print("There's no need for cooling and heating!")

    
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='control Air Conditioner')
    parser.add_argument("--input_month",help=" ")
    parser.add_argument("--input_initial_temp",help=" ")
    args=parser.parse_args()
    input_month=args.input_month
    input_initial_temp=args.input_initial_temp
    main(month, input_initial_temp)
