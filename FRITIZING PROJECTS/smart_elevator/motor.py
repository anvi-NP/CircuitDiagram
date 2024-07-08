import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
Ena,In1,In2 = 29, 31, 36
GPIO.setup(Ena,GPIO.OUT)
GPIO.setup(In1,GPIO.OUT)
GPIO.setup(In2,GPIO.OUT)
pwm = GPIO.PWM(Ena, 100)
pwm.start(0)
GPIO.output(Ena,GPIO.HIGH)
try:
    while True:
        GPIO.output(In1,GPIO.HIGH)
        GPIO.output(In2,GPIO.LOW)
        pwm.ChangeDutyCycle(99)
    GPIO.cleanup()
finally:
    GPIO.cleanup()
