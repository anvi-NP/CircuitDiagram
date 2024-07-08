import RPi.GPIO as GPIO
import LCD1602
from mfrc522 import SimpleMFRC522
import time

LCD1602.init(0x27, 1)
GPIO.setmode(GPIO.BOARD)
trig_pin = 16
echo_pin = 18
floor_0 = 1.6
floor_1 = 7.0
floor_2 = 13.0
Ena, In1, In2 = 29, 31, 36

GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

GPIO.setup(Ena,GPIO.OUT)
GPIO.setup(In1,GPIO.OUT)
GPIO.setup(In2,GPIO.OUT)
pwm = GPIO.PWM(Ena, 100)
pwm.start(0)

GPIO.output(Ena,GPIO.HIGH)




def display_lcd(text):
    LCD1602.clear()
    LCD1602.write(0,0,f"{text}")
    
def distance():
    GPIO.output(trig_pin,0)
    time.sleep(2E-6)
    GPIO.output(trig_pin,1)
    time.sleep(10E-6)
    GPIO.output(trig_pin,0)
    while GPIO.input(echo_pin)==0:
        pass
    echo_start_time = time.time()
    while GPIO.input(echo_pin)==1:
        pass
    echo_stop_time = time.time()
    ping_travel_time = echo_stop_time - echo_start_time
    distance = (767*ping_travel_time*5280*12/3600)/2
    print(round(distance,1), 'Inches')
    time.sleep(.1)
    return distance

def motor_forward():
    pwm.ChangeDutyCycle(99)
    GPIO.output(In1,GPIO.HIGH)
    GPIO.output(In2,GPIO.LOW)
    
    
def motor_backward():
    pwm.ChangeDutyCycle(99)
    GPIO.output(In1,GPIO.LOW)
    GPIO.output(In2,GPIO.HIGH)

def motor_stop():
    #GPIO.output(In1,GPIO.LOW)
    #GPIO.output(In2,GPIO.LOW)
    pwm.ChangeDutyCycle(0)

def back_to_ground():
    
    display_lcd("Going To Floor 0")
    motor_backward()
    while distance() <= floor_0:
        pass
    display_lcd("Floor 0 Reached")
    motor_stop()
    
def change_floor(floor, f):
    display_lcd(f"Going To Floor {f}")
    #motor_forward()
    dist = distance()
    print(f"Going Floor {f}")
    if dist > floor:
            motor_backward()
    elif dist < floor:
            motor_forward()
    while True:
        dist = distance()
        if abs(dist - floor) < 0.5:
            print("STOPPPEDDDDD")
            motor_stop()
            display_lcd(f"Floor {f} Reached")
            break
        time.sleep(.1)

try:
    reader = SimpleMFRC522()
    while True:
        display_lcd("Show Card")
        id, role = reader.read()
        print(id, role)
        print(type(id))
        if (id == 193590607846):
            change_floor(floor_1, "1")
            time.sleep(5)
            change_floor(floor_0,"0")
            #back_to_ground()
            #motor_backward()
            #display_lcd("Back to ground")
            #time.sleep(3)
            #motor_stop()
                
           
        elif (id == 691832429507):
            change_floor(floor_1, "2")
            time.sleep(5)
            change_floor(floor_0,"0")
            
        else:
            display_lcd("Access Denied")
        time.sleep(4)
        
except KeyboardInterrupt:
    time.sleep(.2)
    LCD1602.clear()
    print("good to go")
finally:
    LCD1602.clear()
    GPIO.cleanup()
