import RPi.GPIO as gpio
import time

def init():
 gpio.setmode(gpio.BCM)
 gpio.setup(17, gpio.OUT)
 gpio.setup(18, gpio.OUT)
 gpio.setup(23, gpio.OUT)
 gpio.setup(24, gpio.OUT)

def forward(sec):
 init()
 gpio.output(17, True)
 gpio.output(18, False)
 gpio.output(23, True) 
 gpio.output(24, False)
 time.sleep(sec)
 gpio.cleanup()

def reverse(sec):
 init()
 gpio.output(17, False)
 gpio.output(18, True)
 gpio.output(23, False) 
 gpio.output(24, True)
 time.sleep(sec)
 gpio.cleanup()

def turn_left(sec):
 init()
 gpio.output(17, True)
 gpio.output(18, True)
 gpio.output(23, True) 
 gpio.output(24, False)
 time.sleep(sec)
 gpio.cleanup()

def turn_right(sec):
 init()
 gpio.output(17, True)
 gpio.output(18, False)
 gpio.output(23, False) 
 gpio.output(24, False)
 time.sleep(sec)
 gpio.cleanup()

def rev_left(sec):
 init()
 gpio.output(17, False)
 gpio.output(18, False)
 gpio.output(23, False) 
 gpio.output(24, True)
 time.sleep(sec)
 gpio.cleanup()
 
def rev_right(sec):
 init()
 gpio.output(17, False)
 gpio.output(18, True)
 gpio.output(23, True) 
 gpio.output(24, True)
 time.sleep(sec)
 gpio.cleanup()


forward(2)
#turn_left(1)
#turn_right(1)
#rev_left(.60)

