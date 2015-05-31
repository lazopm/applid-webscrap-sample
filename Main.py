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
def updatePercentage():
    global t
    global range_size
    global counter
    counter+=1
    percent = floored_percentage(counter/range_size, 2)
    sys.stdout.flush()
    print (percent+"                "+str(rut)+"   Velocity: "+str(speed), end="        \r")
def updateKey():
    global t, key, counter, pcounter, speed
    speed = floor(((counter-pcounter)/40)*10)/10
    pcounter = counter
    key = Keymaker.generate()
    t=Timer(40.0,updateKey)
    t.start()
def mainloop(rut):
    if rut in all_ruts:
        return 1
    else:
        result = Extractor.http_request(rut,key)
        if result==0:
            return 2
        else:
            return result

print("Rut Extractor")
start=int(input("Range Start:"))
end=int(input("Range End:"))
thread_number=int(input("Threads:"))
all_ruts=Uploader.getruts(start, end)
counter=0
pcounter=0
finished=0
t=None
print ("Checking database...                "+'\r', end="")
all_ruts = Uploader.getruts(start, end)
range_size=end-start
sys.stdout.flush()
print ("Cracking captcha key...                "+'\r', end="")
updateKey()
start_time=time.time()
sys.stdout.flush()
print ("Setting up Queue...              "+'\r', end="")
with concurrent.futures.ThreadPoolExecutor(max_workers=thread_number) as executor:
    future_to_result = {executor.submit(mainloop, rut): rut for rut in range(start, end)}
    for future in concurrent.futures.as_completed(future_to_result):
        rut = future_to_result[future]
        try:
            data = future.result()
        except Exception as exc:
            print("Rut "+str(rut)+" raised an exception.")
            updatePercentage()
        else:
            if data==1:
                updatePercentage()
            elif data==2:
                print("Rut "+str(rut)+" timed out.")
                updatePercentage()
            else:
                if Process.validate(data) == 1:
                    global key
                    key = Keymaker.generate()
                    time.sleep(5)
                    updatePercentage()
                else:
                    Uploader.updata(rut,Process.process(data))
                    updatePercentage()
    t.cancel()
    print(time.time()-start_time)