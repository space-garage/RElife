from Tkinter import *

class MainPanel(object):

    def Start(self, event):
        if self.startFirtsRun:
            self.startFirtsRun=False
            self.state[2]=self.testEnt.get()
            self.state[3]=self.nameEnt.get()
            self.R1.state=DISABLED
        if (self.state[0]!='proceed'):
            self.state[0]='start'

            print 'start'
        
    def Stop(self, event):

        if (self.state[0]!='stoped'):
            self.state[0]='stop'
            print 'stop'
        
    def New_test(self):
        self.state[0]='New_test'
        self.startFirtsRun = True
        print 'New_test'
        

    def Ev1(self, event):
        self.state[1]='Ev1'
        print 'Ev1'
        #print self.info.get()
        

    def Ev2(self, event):
        self.state[1]='Ev2'
        print 'Ev2'

    def Ev3(self, event):
        self.state[1]='Ev3'
        print 'Ev3'
        
    def Flush(self, event):
        self.state[0]='Flush'
        print 'Flush'
        self.root.destroy()

    def sel(self):
        print "You selected the option " + self.var.get()
        
        self.testEnt.delete(0,len(self.testEnt.get()))
        if self.var.get() != 'Custom':
            self.testEnt.insert ( 0, self.var.get() )
       #selection = "You selected the option " + str(var.get())
       #label.config(text = selection)
        
    def butcallb(self,butstr):
        
            
        self.state[1]=butstr
        print butstr
        
    def __init__(self,vall):
        self.root = Tk()
        self.startFirtsRun = True
        self.state=vall

        frame = Frame(self.root, width=410, height=300)
        frame.pack_propagate(0) # set the flag to use the size
        frame.pack() # remember to pack it or else it will not be pack

        cBP={'x':10,'y':50, 'xbp':80, 'ybp':35} #controlBlockPos xbp-x_button_period
        startData = Button(self.root, text = 'Start_data')
        startData.place(x = cBP['x'], y = cBP['y'], width = 75, height = 30)
        stopData = Button(self.root, text = 'Stop_data')
        stopData.place(x = cBP['x']+cBP['xbp'], y = cBP['y'], width = 75, height = 30)
        Flush = Button(self.root, text = 'Flush')
        Flush.place(x = cBP['x']+cBP['xbp']*2, y = cBP['y'], width = 75, height = 30)
        newTest = Button(self.root, text = 'New_Test', command=self.New_test)
        newTest.place(x = cBP['x']+cBP['xbp']*4, y = cBP['y'], width = 75, height = 30)        


        tBP={'x':10,'y':90, 'xbp':80, 'ybp':35}#testBlockPos xbp-x_button_period
        self.var=StringVar()
        self.testEnt=Entry(self.root, width=40,text="test")
        self.testEnt.place(x=tBP['x']+60,y=tBP['y'])

        lb=Label(text="test")
        lb.place(x=tBP['x'], y=tBP['y'])
        
        self.R1 = Radiobutton(self.root, text="tetris", variable=self.var, value='tetris', command=self.sel)        
        self.R1.place( x = tBP['x'], y = tBP['y']+30 )
        R2 = Radiobutton(self.root, text="Stroop", variable=self.var, value='stroop', command=self.sel)        
        R2.place( x = tBP['x']+tBP['xbp'], y = tBP['y']+30 )
        R3 = Radiobutton(self.root, text="IQ", variable=self.var, value='IQ', command=self.sel)        
        R3.place( x = tBP['x']+tBP['xbp']*2, y = tBP['y']+30 )
        R4 = Radiobutton(self.root, text="Pub. spk", variable=self.var, value='Pub. spk', command=self.sel)       
        R4.place( x = tBP['x']+tBP['xbp']*3, y = tBP['y']+30 )
        R5 = Radiobutton(self.root, text="Custom", variable=self.var, value='Custom', command=self.sel)        
        R5.place( x = tBP['x']+tBP['xbp']*4, y = tBP['y']+30 )
        self.R1.invoke() #deselect()
        
        #tetris but
        tet=Button(self.root, text = 'bsLnClt', command=lambda: self.butcallb('bsLnClt'), bg="green")
        tet.place(x = tBP['x'], y = tBP['y']+60, width = 75, height = 30)
        tet=Button(self.root, text = 'tWrBhw', command=lambda: self.butcallb('tWrBhw'))
        tet.place(x = tBP['x'], y = tBP['y']+60+tBP['ybp'], width = 75, height = 30)

        #stroop
        stroop=Button(self.root, text = 'WrngAns', command=lambda: self.butcallb('WrngAns'))
        stroop.place(x = tBP['x']+tBP['xbp'], y = tBP['y']+60, width = 75, height = 30)

        #IQ
        iqbnq=Button(self.root, text = 'NewQst', command=lambda: self.butcallb('NewQst'))
        iqbnq.place(x = tBP['x']+tBP['xbp']*2, y = tBP['y']+60, width = 75, height = 30)

        iqbwra=Button(self.root, text = 'WrngAsn', command=lambda: self.butcallb('WrngAsn'))
        iqbwra.place(x = tBP['x']+tBP['xbp']*2, y = tBP['y']+60+tBP['ybp'], width = 75, height = 30)

        iqb=Button(self.root, text = 'TmROut', command=lambda: self.butcallb('TmROut'))
        iqb.place(x = tBP['x']+tBP['xbp']*2, y = tBP['y']+60+tBP['ybp']*2, width = 75, height = 30)

        #Public speaking
        psb1=Button(self.root, text = 'SpStart', command=lambda: self.butcallb('SpStart'))
        psb1.place(x = tBP['x']+tBP['xbp']*3, y = tBP['y']+60, width = 75, height = 30)

        psb1=Button(self.root, text = 'SpQts', command=lambda: self.butcallb('SpQts'))
        psb1.place(x = tBP['x']+tBP['xbp']*3, y = tBP['y']+60+tBP['ybp'], width = 75, height = 30)


        #custom test
        M1 = Button(self.root, text = 'Marker 1')
        M1.place(x = tBP['x']+tBP['xbp']*4, y = tBP['y']+60, width = 65, height = 30)
        M2 = Button(self.root, text = 'Marker 2')
        M2.place(x = tBP['x']+tBP['xbp']*4, y = tBP['y']+60+tBP['ybp'], width = 65, height = 30)
        M3 = Button(self.root, text = 'Marker 3')
        M3.place(x = tBP['x']+tBP['xbp']*4, y = tBP['y']+60+tBP['ybp']*2, width = 65, height = 30)        



        nBP={'x':10,'y':10}#nameBlockPos
        nmLb=Label(text="Name")
        nmLb.place(x=nBP['x'], y=nBP['y'])
        self.nameEnt=Entry(self.root, width=40,text="Name")
        self.nameEnt.place(x=nBP['x']+60,y=nBP['y'])


        print type(startData)
        
        startData.bind("<Button-1>", self.Start)
        stopData.bind("<Button-1>", self.Stop)
        M1.bind("<Button-1>", self.Ev1)
        M2.bind("<Button-1>", self.Ev2)
        M3.bind("<Button-1>", self.Ev3)
        Flush.bind("<Button-1>", self.Flush)
        
    def StartLoop(self):
        self.root.mainloop()


if __name__ == '__main__' :
    import threading
    a=[None,None,None,None]
    print id(a),a
    #kb=MainPanel(a)
    
    #t_panel=threading.Thread(target=kb.StartLoop, args=())
    #t_panel.start()
    qw=MainPanel(a)
    qw.StartLoop()
    
