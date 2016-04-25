#-*- coding: utf-8 -*-
import re
import json
import subprocess
from time import sleep
from multiprocessing import Process,Queue
sequence = [u'Десять', u'Девять', u'Восемь', u'Семь', u'Шесть', u'Пять', u'Четыре',u'Три',u'Два',u'Один']
#sequence_files = ['10.wav','09.wav','08.wav','07.wav','06.wav','05.wav','04.wav','03.wav','02.wav','01.wav']
sequence_files = ['05.wav','04.wav','03.wav','02.wav','01.wav']

def tts2(file):
    #faster playing of predefined sentences
    subprocess.call(['/usr/bin/aplay',file])

def google_command(q):
        while(True):
                try:
			lines= subprocess.check_output(['/home/pi/google-command.sh'])
			for line in lines.splitlines():
			    result = json.loads(line)
			    if(len(result[u'result'])>0):
			       res = result[u'result'][0][u'alternative'][0]
			       q.put({'type': 'AUDIO', 'value': res[u'transcript']})
		except(KeyError,ValueError,subprocess.CalledProcessError):
			pass

def tts(s):
    #call to festival client
    p=subprocess.Popen('/usr/bin/festival_client',stdin=subprocess.PIPE,stdout=None)
    str = u'(SayText "%s")'
    s.encode('utf-8')
    x=str % s
    print x
    p.communicate(x.encode('utf-8'))
    p.stdin.close()

def button_process(q):
    while(True):
	    with open("/sys/class/gpio/gpio4/value") as f:
	       val=f.read()
	       sleep(1)
	       if(val.strip()=='0'):
		  q.put({'type':'BUTTON','value': 1})

def inject():
    pass
    
if __name__ == '__main__':
    tts(u"Система готова!")
    q=Queue()
    p = Process(target=google_command,args=(q,))
    p.start()
    p1 = Process(target=button_process,args=(q,))
    p1.start()
    while(True):
       message = q.get()
       if(message['type']=='AUDIO'):
           print message['value']
           #tts(u"Распознано: "+message['value'])
           #tts(message['value'])
           if(re.search(u'глицерин',message['value']) or re.search(u'Нитроглицерин',message['value'])):
             #tts(u"Команда нитроглицерин. Через 10 секунд - укол нитроглицерина")
             tts2('nitro.wav')
             sleep(2)
             #tts(u"Скажите отмена для отмены")
             tts2('saycancel.wav')
             cancelled = False
             for count in sequence_files:
                sleep(3)
                if(not q.empty()):
                  mes=q.get()
                  if(mes['type']=='AUDIO' and re.search(u'мена',mes['value'])):
                    cancelled=True
                    print "Break EXPECTED!"
                    break
                tts2(count)
             if(not cancelled):
                inject()
                tts2('nitro_done.wav')
                pass
             else:
                tts2('cancelled.wav')
             
       print message
    p.join()
    p1.join()


