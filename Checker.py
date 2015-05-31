import Keymaker
import Extractor
import Process
import Uploader
import sys
import concurrent.futures
import time
from math import floor
from threading import Timer
def floored_percentage(val, digits):
    val *= 10 ** (digits + 2)
    return '{1:.{0}f}%'.format(digits, floor(val) / 10 ** digits)
def updatePercentage(rut):
    global end
    percent = floored_percentage(rut/end, 2)
    sys.stdout.flush()
    print (percent+'             '+str(rut), end="\r")
def updateKey():
    if finished == 0:
        global key
        key = Keymaker.generate()
        t=Timer(40.0,updateKey)
        t.start()
    else:
        "Goodbye!"
def mainloop(rut):
    return Extractor.http_request(rut,key)
counter=0
finished=0
print("Rut Checker")
start=int(input("Range Start:"))
end=int(input("Range End:"))
print ("Cracking captcha key...                "+'\r', end="")
updateKey()
start_time=time.time()
sys.stdout.flush()
print ("Starting...              "+'\r', end="")
for rut in range(start, end):
    if Uploader.checkrut(rut)==0:
        print("Doing missing rut "+str(rut))
        data = Extractor.http_request(rut,key)
        if data==0:
            print("Rut "+str(rut)+" timed out.")
            updatePercentage(rut)
        else:
            if Process.validate(data) == 1:
                key = Keymaker.generate()
                time.sleep(5)
                print("Rut "+str(rut)+" broken key.")
            else:
                Uploader.updata(rut,Process.process(data))
    updatePercentage(rut)






