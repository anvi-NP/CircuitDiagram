import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

reader = SimpleMFRC522()
print("Place the tag")

try:
    while True:
        id = reader.read()
        print(id)
        sleep(2)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()