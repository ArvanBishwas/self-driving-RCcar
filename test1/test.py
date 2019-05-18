import RPi.GPIO as gpio
import time
from motor_control import forward, rev_left
 
 
def distance():
    gpio.setmode(gpio.BCM)

    GPIO_TRIGGER = 21
    GPIO_ECHO = 20

    gpio.setup(GPIO_TRIGGER, gpio.OUT)
    gpio.setup(GPIO_ECHO, gpio.IN)
    gpio.output(GPIO_TRIGGER, True)
 
    time.sleep(0.00001)
    gpio.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
    
    while gpio.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    while gpio.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 

    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34300) / 2   
    return distance
 


 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            if dist < 10:
                rev_left(.30)
                print("To close = ", dist)
                
            else:
                forward(.10)
                print("Distance = %1f " %dist)
                
    except KeyboardInterrupt:
            print("Measurement stopped by User")
            gpio.cleanup()
