
import numpy  # Import numpy
import matplotlib.pyplot as plt #import matplotlib library
from drawnow import *

import threading
import struct
import time

import sys

couveNum=12

plt.ion() #Tell matplotlib you want interactive mode to plot live data
self_y = [[] for _ in range(couveNum)]
value=[]
counter=0
lnIndexer = ('b^-','c^-','m^-','k^-','yo-','go-','bo-','co-','mo-','k^-','y^-','b^-')

'''
0, 'b^-',
1, 'c^-', magic GSR chanel
2, 'm^-', GSR chan
3, 'k^-',
4, 'yo-',
5, 'go-',
6, 'bo-',
7, 'co-', 
8, 'mo-', body temp
9, 'k^-', out temp
10,'y^-', magic channel range
11,'b^-', giro
'''

def makeFig(): #Create a function that makes our desired plot
    global couveNum, counter

    map(lambda a, b: a.append(b), self_y, value)

    plt. plot( self_y[1], lnIndexer[1], label='Panic' )
    plt. plot( self_y[2], lnIndexer[2], label='Panic owerview' )
    plt. plot( self_y[8], lnIndexer[8], label='body temp' )
    plt. plot( self_y[9], lnIndexer[9], label='out temp' )
    plt. plot( self_y[10], lnIndexer[10], label='Panic range' )
    plt. plot( self_y[11], lnIndexer[11], label='Movement act.' )
    plt.legend(loc='upper left')  
    #plt.draw()

    #for i in range(couveNum):
        
        #plt. plot( self_y[i], lnIndexer[i] )  #25
        #plt.draw()
    if (counter > 40):
        map(lambda a: a.pop(0), self_y)
    counter+=1

while True:
    word = sys.stdin.readline().rstrip()

    value = word.split(',')

    drawnow(makeFig,show_once=False)
    plt.pause(.0001) 



sys.exit()



