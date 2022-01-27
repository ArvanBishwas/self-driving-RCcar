# -*- coding: utf-8 -*-

# Raspberry Pi pin (BCM number) to which the DC motor is connected
LEFT_PIN_A = 17
LEFT_PIN_B = 18
LEFT_PWM = 0
RIGHT_PIN_A = 23
RIGHT_PIN_B = 24
RIGHT_PWM = 27

# speed regulation of the car
GEARS = [0, 1, 2, 3, 4]

# Define the operation command
STOP     = 0b0000
LEFT     = 0b0001
RIGHT    = 0b0010
FORWARD  = 0b0100
BACKWARD = 0b1000
SHUTDOWN = 0b1111

SERVER_HOST = "0.0.0.0"
PI_HOST = "192.168.0.7"
COMPUTER_HOST = "192.168.0.11"
VIDEO_STREAMING_PORT = 8000
KEYBOARD_PORT = 8001
