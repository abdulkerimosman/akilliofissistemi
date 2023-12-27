#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
pin_to_circuit = 37
relay_pin = 36  # Change this to the GPIO pin connected to your relay

# Set up the relay pin
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, GPIO.LOW)
 # Initially, turn the light on

def rc_time(pin_to_circuit):
    count = 0

    # Output on the pin for
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    # Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)

    # Count until the pin goes high
    while GPIO.input(pin_to_circuit) == GPIO.LOW:
        count += 1

    return count

# Catch when the script is interrupted, cleanup correctly
try:
    # Main loop
    while True:
        light_level = rc_time(pin_to_circuit)

        # Adjust the threshold value according to your needs
        threshold = 7000  # You may need to experiment with this value

        if light_level < threshold:
            # It is dark, turn off the light
            GPIO.output(relay_pin, GPIO.LOW)
        else:
            # It is bright, turn on the light
            GPIO.output(relay_pin, GPIO.HIGH)

        print(f"direnç: {light_level}")
        time.sleep(1)  # Adjust the sleep duration as needed

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
