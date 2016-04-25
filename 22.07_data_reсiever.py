import serial # import Serial Library
import numpy  # Import numpy
import time 
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *
from struct import *
import threading

e1 = threading.Event()

gyrAcc=0

ADC1=[]
ADC2=[]
ADC3=[]
ADC4=[]
ADC5=[]
ADC6=[]
ADC7=[]
ADC8=[]
GYRO=[]

pltADC=[[],[],[],[],[],[],[],[],[]]
soc=[]
arduinoData = serial.Serial('com5', 38400) #Creating our serial object named arduinoData
plt.ion() #Tell matplotlib you want interactive mode to plot live data
cnt=0

def makeFig(): #Create a function that makes our desired plot
    #plt.ylim(0,0x1000)                                 #Set y min and max values
    plt.title('My Live ADC Data')      #Plot the title
    plt.grid(True)                                  #Turn the grid on
    #plt.ylabel('ADC1')                            #Set ylabels


    plt.plot(pltADC[0], 'ro-', label='ADC1')       #plot the temperature
                                                    #plot the legend
    plt.plot(pltADC[1], 'b^-', label='ADC2')
    plt.plot(pltADC[2], 'c^-', label='ADC3') #plot ADC2 data
    plt.plot(pltADC[3], 'm^-', label='ADC4') #plot ADC2 data
    plt.plot(pltADC[4], 'k^-', label='ADC5') #plot ADC2 data
    plt.plot(pltADC[5], 'yo-', label='ADC6') #plot ADC2 dataArray
    plt.plot(pltADC[6], 'go-', label='ADC7') #plot ADC2 data
    plt.plot(pltADC[7], 'bo-', label='ADC8') #plot ADC2 data
    
    plt.legend(loc='upper left')

    plt2=plt.twinx()
    plt2.plot(pltADC[8], 'co-', label='GYRO') #plot ADC2 data
    plt2.set_ylabel('Gyro')
c=0

def tread(soc,event):
    while True:
        event.wait()
        #print 'event.wait()'
        event.clear()
        #print soc
        #print pltADC
        #print ADC1

        drawnow(makeFig)                       #Call drawnow to update our live graph
        plt.pause(.000001)                     #Pause Briefly. Important to keep drawnow from crashing
        #cnt=cnt+1


t1 = threading.Thread(target=tread, args=(soc,e1))
 
start_seq =  (((time.clock())))

print 'before tread starts'
t1.start()

#while (arduinoData.inWaiting()==0): #Wait here until there is data
#    pass #do nothing
#arduinoString = arduinoData.readline() #read the line of text from the serial port
    

while c<20000: # While loop that loops forever
    while (arduinoData.inWaiting()==0): #Wait here until there is data
        pass #do nothing
    arduinoString = arduinoData.read(18) #read the line of text from the serial port
    dataArray = unpack('HHHHHHHHH',arduinoString)#arduinoString.split(',')   #Split it into an array called dataArray
    ADC1.append(int( dataArray[0]))            #Convert first element to floating number and put in temp
    ADC2.append(int( dataArray[1]))            #Convert second element to floating number and put in P
    ADC3.append(int( dataArray[2]))
    ADC4.append(int( dataArray[3]))
    ADC5.append(int( dataArray[4]))
    ADC6.append(int( dataArray[5]))
    ADC7.append(int( dataArray[6]))
    ADC8.append(int( dataArray[7]))
    GYRO.append((int( dataArray[8])))
    c+=1
    if (c%100==0):
        #print GYRO[-1]
        
        gyrAcc=(reduce(lambda a, x: abs(16000-a) + x, GYRO[-99:]))/1000
        
        
        soc=[ADC1[-1] - 600,ADC2[-1] - 600,ADC3[-1] - 600,ADC4[-1] - 600,\
        ADC5[-1] - 600,ADC6[-1] - 600,ADC7[-1] - 600,ADC8[-1] - 600,gyrAcc]
        print soc
        for i in range(9):
            pltADC[i].append(soc[i])
        cnt+=1
        if(cnt>40):                            #If you have 50 or more points, delete the first one from the array
            for i in range(9):
                pltADC[i].pop(0)                       #This allows us to just see the last 50 data points
            
        e1.set()
        
end_seq =  (((time.clock())))



#print ADC1
print 'collects ', c, 'samples'
print 'during', (start_seq-end_seq),'s'
mADC=[]
mADC.append(ADC1)
mADC.append(ADC2)
mADC.append(ADC3)
mADC.append(ADC4)
mADC.append(ADC5)
mADC.append(ADC6)
mADC.append(ADC7)
mADC.append(ADC8)
mADC.append(GYRO)
with open('data.csv', 'w') as f:
    for i in range(len(mADC[0])):
        #f.write('\n')
        #f.write('ADC'+str(i+1)+':')
        for x in range(9):
            f.write(str((mADC[x])[i]) + ',')
        f.write('\n')
    f.write('collects '+ str(c)+ ' samples')
    f.write('during '+ str(start_seq-end_seq)+' s')
print 'done'

'''
    drawnow(makeFig)                       #Call drawnow to update our live graph
    plt.pause(.000001)                     #Pause Briefly. Important to keep drawnow from crashing
    cnt=cnt+1
    if(cnt>40):                            #If you have 50 or more points, delete the first one from the array
        ADC1.pop(0)                       #This allows us to just see the last 50 data points
        ADC2.pop(0)
        ADC3.pop(0)
        ADC4.pop(0)
        ADC5.pop(0)
        ADC6.pop(0)
        ADC7.pop(0)
        ADC8.pop(0)
'''
