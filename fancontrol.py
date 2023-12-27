import RPi.GPIO as GPIO
import dht11
import time
import datetime

# Initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# Fan control GPIO pin
FAN_PIN = 6  # Change this to the GPIO pin you're using for the fan
GPIO.setup(FAN_PIN, GPIO.OUT)
GPIO.output(FAN_PIN, GPIO.LOW)  # Start with the fan off

# DHT11 setup
instance = dht11.DHT11(pin=5)

# Temperature threshold for fan activation
TEMP_THRESHOLD = 25.0  # Adjust this to your desired threshold

try:
    while True:
        result = instance.read()
        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))

            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)

            # Check if the temperature is above the threshold
            if result.temperature > TEMP_THRESHOLD:
                print("Temperature above threshold. Turning on the fan.")
                GPIO.output(FAN_PIN, GPIO.HIGH)  # Turn on the fan
            else:
                print("Temperature below threshold. Turning off the fan.")
                GPIO.output(FAN_PIN, GPIO.LOW)  # Turn off the fan

        #time.sleep(0)
  
except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()
