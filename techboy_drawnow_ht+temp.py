# -*- coding: cp1251 -*-
sim=False
if not sim:
    import serial # import Serial Library
import numpy  # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *
from gtk_new import *
import threading
import struct 
import time
import os
import subprocess
import sys

'''
from hot_key import *

print 'Ctrl + Shift + 5 Start'
print 'Ctrl + Shift + 6 Stop'
print 'Ctrl + Shift + 1 Ev1'
print 'Ctrl + Shift + 2 Ev2'
print 'Ctrl + Shift + 3 Ev3'
print 'Ctrl + Shift + 4 Flush'
'''


child = os.path.join(os.path.dirname('__file__'), "./chil_drawnow.py")
#child = 'C:\Users\Vasiliy\Documents\@pmpr\Pthn_Wbnd\chil_drawnow.py'



command = [sys.executable, child]
pipe = subprocess.Popen(command,
stdout=subprocess.PIPE,
stderr=subprocess.PIPE,
stdin=subprocess.PIPE,
)

couveNum=12

class dummy(object):
    def write(self,stri):
        return None
    def inWaiting(self):
        return 1
    def read(self,inu):
        return 'asdfghjklpoiuytrew782356'
    def write(self,inu):
        return None
    def close(self):
        return None
    
if not sim:
    WBSerObj = serial.Serial('com4', 38400, timeout=5 ) #Creating our serial object named arduinoData
else:
    WBSerObj=dummy()

#WBSerObj = serial.Serial('com4', 38400) #Creating our serial object named arduinoData
print 'Connection scsfl'

evList=['star',"",'','']



def panelTread(evList):
    panel=MainPanel(evList)
    panel.StartLoop()
t_panel=threading.Thread(target=panelTread, args=(evList,))
t_panel.start()

'''


def htkTread(evList):
    htk=HotKeys(evList)
    htk.StartLoop()
t_htk=threading.Thread(target=htkTread, args=(evList,))
t_htk.start()
'''



WBdatas = [[] for _ in range(couveNum+1)] # We add one extra to fill it with time and events later.

value=[]
'''
plt.ion() #Tell matplotlib you want interactive mode to plot live data
lnIndexer = ('b^-','c^-','m^-','k^-','yo-','go-','bo-','co-','mo-','k^-')
self_y = [[] for _ in range(couveNum)]
value=[]
counter=0

def makeFig(): #Create a function that makes our desired plot
    global couveNum, counter

    map(lambda a, b: a.append(b), self_y, value)
    for i in range(couveNum):
              
        plt. plot( self_y[i], lnIndexer[i] )  #25
        #plt.draw()
    if (counter > 40):
        map(lambda a: a.pop(0), self_y)
    counter+=1


e1 = threading.Event()
e1.clear()

def Grd(ev):
    while True:
        ev.wait() # wait for event
        ev.clear()
        drawnow(makeFig,show_once=False)#
        plt.pause(.0001)
t_Grd=threading.Thread(target=Grd, args=(e1,))
t_Grd.start()
'''
c=0
def WrFile():
    global c
    with open((time.asctime().replace(' ','_').replace(':','-'))+' '+evList[2]+' '+evList[3]+'.csv', 'w') as f:
        for i in range(len(WBdatas[0])):
            #f.write('\n')
            #f.write('ADC'+str(i+1)+':')
            for x in range(couveNum+1):
                f.write(str((WBdatas[x])[i]) + ',')
            f.write('\n')
        f.write('collects '+ str(c)+ ' samples')
        #f.write('during '+ str(start_seq-end_seq)+' s')
        f.close()
    print 'done'
    c=0


print "before main loop"
    
while (evList[0]!='Flush'):
    if (evList[0]=='start'):
        WBSerObj.write('startzzz')
        evList[0]='proceed'
        #plt.close()
        print evList[0]
        
    if (evList[0]=='New_test'):
        WrFile()
        print 'data have writtten in file'
        for d in WBdatas: #del WBdatas -> [[],[],...]
            del d[:]
        evList[0]='stop'
        #map(lambda a: (del a[:]), WBdatas) ::)))
        print 'Ready for new test, data flow stoped'
        
    if ((evList[0]=='stop')):
        WBSerObj.write('stopzzzz')
        evList[0]='stoped'
        #plt.close()
        #drawnow(makeFig,show_once=True)

    if (evList[0]=='proceed'): # While loop that loops 
        while (WBSerObj.inWaiting()==0): #Wait here until there is data
            pass #do nothing
        WBString = WBSerObj.read(couveNum*2) #read the line of text from the serial port

        if len(WBString) != couveNum*2: #Make forcibly flush if transmition fails. 
            WBString= 'a' * couveNum*2
            evList[0]='Flush'
            print "Com read time out have occurred, flush initiated forcibly"
            
        WBdataTpl = struct.unpack('H'*couveNum,WBString)#arduinoString.split(',')   #Split it into an array called dataArray

        map(lambda a,b: a.append(b), WBdatas,WBdataTpl)
        
        if (c%100==0):
            if sim:
                time.sleep(1)
            #del value[:]
            value.extend(WBdataTpl)
            value[-1]=((reduce(lambda a, x: abs(16000-a) + x, WBdatas[couveNum-1][-99:]))/1000) #smooth  gyro data

            print WBdataTpl
            #print (','.join(str(x) for x in value).encode("utf8") + b"\n")
            pipe.stdin.write(','.join(str(x) for x in value).encode("utf8") + b"\n")
            
            del value[:]
             
            
            WBdatas[-1][-1]=time.asctime()[11:20:]+evList[1] 
            #WBdatas[8][-1]=((WBdatas[8][-1]>>4)+(WBdatas[8][-1]&7)*0.0625)
            #WBdatas[9][-1]=((WBdatas[9][-1]>>4)+(WBdatas[9][-1]&7)*0.0625)
            evList[1]=''
            
        c+=1   

WBSerObj.write('stopzzzz')
WrFile()
#plt.close()
pipe.stdin.close()

WBSerObj.close()
'''
with open((time.asctime().replace(' ','_').replace(':','-'))+' '+evList[2]+' '+evList[3]+'.csv', 'w') as f:
    for i in range(len(WBdatas[0])):
        #f.write('\n')
        #f.write('ADC'+str(i+1)+':')
        for x in range(couveNum+1):
            f.write(str((WBdatas[x])[i]) + ',')
        f.write('\n')
    f.write('collects '+ str(c)+ ' samples')
    #f.write('during '+ str(start_seq-end_seq)+' s')
    f.close()
print 'done'
'''
