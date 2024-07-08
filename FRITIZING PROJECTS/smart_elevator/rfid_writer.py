import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()



try:
    text = input("Insert Data: ")
    print("Place the tag")
    reader.write(text)
    print("The data is written")
finally:
    GPIO.cleanup()