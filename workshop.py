import Keymaker
import Extractor
import Process
import Uploader
import sys
from concurrent.futures import ThreadPoolExecutor
import time
from math import floor
from threading import Timer
t = None
def floored_percentage(val, digits):
    val *= 10 ** (digits + 2)
    return '{1:.{0}f}%'.format(digits, floor(val) / 10 ** digits)
def updatePercentage(rut):
    global range_size
    global counter
    counter+=1
    percent = floored_percentage(counter/range_size, 2)
    sys.stdout.flush()
    print (percent+"          "+str(rut), end="\r")
def updateKey():
    if finished == 0:
        global key
        global t
        key = Keymaker.generate()
        t=Timer(40.0,updateKey)
        t.start()
    else:
        "Goodbye!"

def mainloop(rut):
    if Uploader.checkrut(rut)==0:
        global key
        #Not in db, request
        result = Extractor.http_request(rut,key)
        if result == 0:
            print ("timed out")
            mainloop(rut)
        else:
            if Process.validate(result)==1:
                print ("broken key")
                key = Keymaker.generate()
                time.sleep(5)
                mainloop(rut)
            else:
                #Valid result
                updatePercentage(rut)
                Uploader.updata(rut,Process.process(result))
    else:
        print("already in db")
        updatePercentage(rut)

counter=0
finished=0
print("Rut Extractor")
start=int(input("Range Start:"))
end=int(input("Range End:"))
thread_number=int(input("Threads:"))
range_size=end-start
sys.stdout.flush()
print ("Cracking captcha key...                "+'\r', end="")
updateKey()
start_time=time.time()
sys.stdout.flush()
print ("Starting...              "+'\r', end="")
with ThreadPoolExecutor(max_workers=thread_number) as e:
    e.map(mainloop, range(start, end))
t.cancel()