
# -*- coding: utf-8 -*-

import os
import RPi.GPIO as GPIO
import socket
import struct
import sys

from setting import *


class Wheel(object):
    def __init__(self, pin_e, pin_a, pin_b):
        self.PIN_E = pin_e
        self.PIN_A = pin_a
        self.PIN_B = pin_b
        GPIO.setup(self.PIN_E, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.PIN_A, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.PIN_B, GPIO.OUT, initial=GPIO.LOW)
        # PWM frequency initialized to 100Hz, Duty Cycle is initialized to 100%
        self.pwm = GPIO.PWM(self.PIN_E, 100)
        self.pwm.start(100)
        # Car speed gear
        self.gear = 0

    def forward(self):
        GPIO.output(self.PIN_A, GPIO.HIGH)
        GPIO.output(self.PIN_B, GPIO.LOW)

    def backward(self):
        GPIO.output(self.PIN_A, GPIO.LOW)
        GPIO.output(self.PIN_B, GPIO.HIGH)

    def speed_up(self):
        if self.gear < len(GEARS) - 1:
            self.gear += 1
            self.pwm.ChangeDutyCycle(100 * self.gear / (len(GEARS) - 1))

    def slow_down(self):
        if self.gear > 0:
            self.gear -= 1
            self.pwm.ChangeDutyCycle(100 * self.gear / (len(GEARS) - 1))

    def stop(self):
        GPIO.output(self.PIN_A, GPIO.LOW)
        GPIO.output(self.PIN_B, GPIO.LOW)


class Car(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.left_wheel = Wheel(LEFT_PWM, LEFT_PIN_A, LEFT_PIN_B)
        self.right_wheel = Wheel(RIGHT_PWM, RIGHT_PIN_A, RIGHT_PIN_B)
        self.direction = FORWARD
        print("Car is ready!")

    def forward(self):
        self.direction = FORWARD
        self.left_wheel.forward()
        self.right_wheel.forward()

    def backward(self):
        self.direction = BACKWARD
        self.left_wheel.backward()
        self.right_wheel.backward()

    def speed_up(self):
        self.left_wheel.speed_up()
        self.right_wheel.speed_up()

    def slow_down(self):
        self.left_wheel.slow_down()
        self.right_wheel.slow_down()

    def turn_left(self):
        self.left_wheel.stop()
        if self.direction == FORWARD:
            self.right_wheel.forward()
        else:
            self.right_wheel.backward()

    def turn_right(self):
        self.right_wheel.stop()
        if self.direction == FORWARD:
            self.left_wheel.forward()
        else:
            self.left_wheel.backward()

    def forward_left(self):
        self.forward()
        self.turn_left()

    def forward_right(self):
        self.forward()
        self.turn_right()

    def backward_left(self):
        self.backward()
        self.turn_left()

    def backward_right(self):
        self.backward()
        self.turn_right()

    def stop(self):
        self.left_wheel.stop()
        self.right_wheel.stop()

    def shutdown(self):
        self.stop()
        GPIO.cleanup()


class Driver(object):
    def __init__(self):
        self.car = Car()
        self.server_socket = socket.socket()
        self.server_socket.bind((SERVER_HOST, KEYBOARD_PORT))
        self.server_socket.listen(0)
        self.connection = self.server_socket.accept()[0]
        print("Ready to drive!")

    @staticmethod
    def error():
        print("Invalid Operation Code!")

    def drive(self):
        """Drive the car according to the operating instructions"""
        operations = {
            STOP:               self.car.stop,
            LEFT:               self.car.turn_left,
            RIGHT:              self.car.turn_right,
            FORWARD:            self.car.forward,
            FORWARD | LEFT:     self.car.forward_left,
            FORWARD | RIGHT:    self.car.forward_right,
            BACKWARD:           self.car.backward,
            BACKWARD | LEFT:    self.car.backward_left,
            BACKWARD | RIGHT:   self.car.backward_right,
            SHUTDOWN:           self.car.shutdown
        }
        code2str = {
            STOP:               "Stop",
            LEFT:               "Left",
            RIGHT:              "Right",
            FORWARD:            "Forward",
            FORWARD | LEFT:     "Forward Left",
            FORWARD | RIGHT:    "Forward Right",
            BACKWARD:           "Backward",
            BACKWARD | LEFT:    "Backward Left",
            BACKWARD | RIGHT:   "Backward Right",
            SHUTDOWN:           "Shutdown"
        }
        while True:
            code = struct.unpack('<I', self.connection.recv(struct.calcsize('<I')))[0]
            operations.get(code, self.error)()
            print("Take Action: %s" % code2str.get(code, "None"))
            if code == SHUTDOWN:
                sys.exit(0)


if __name__ == "__main__":
    driver = Driver()
    driver.drive()

