#importing libs
import digitalio
import board
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

#Seting the GPIO's and Modes

CLK_PIN = board.GP4
DT_PIN = board.GP3
SW_PIN = board.GP2
clk_last = None
count = 0
totalMode = 3
currentMode = 0

#Setting the Raspberry Pi Pico to USB HID Device to simulate the consumer control and the keyboard, Defining the Input and the output of clock, data and switch.

cc = ConsumerControl(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)

clk = digitalio.DigitalInOut(CLK_PIN)
clk.direction = digitalio.Direction.INPUT

dt = digitalio.DigitalInOut(DT_PIN)
dt.direction = digitalio.Direction.INPUT

sw = digitalio.DigitalInOut(SW_PIN)
sw.direction = digitalio.Direction.INPUT
sw.pull = digitalio.Pull.UP
 
#Defining the time for the while loop 
 
def millis():
    return time.monotonic() * 1000

#Defining the counter clockwise scroll by the modes 

def ccw():
    print("CCW")
    if (currentMode == 0):
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        #Volume down 
    elif(currentMode == 1):
        cc.send(ConsumerControlCode.BRIGHTNESS_DECREMENT)
        #Brightness down
    elif(currentMode == 2):
        keyboard.press(Keycode.LEFT_ARROW)
        keyboard.release_all()
        #Horizontal scroll left - Adobe Premiere Pro
        
#Defining the clockwise scroll by the modes

def cw():
    print("CW")
    if (currentMode == 0):
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        #Volume up
    elif(currentMode == 1):
        cc.send(ConsumerControlCode.BRIGHTNESS_INCREMENT)
        #Brightness up
    elif(currentMode == 2):
        keyboard.press(Keycode.RIGHT_ARROW)
        keyboard.release_all()
        #Horizontal scroll right - Adobe Premiere Pro
        
#Defining the long press function, using custom keyboard shortcut to simply turn off the computer

def long_press():
    keyboard.press(Keycode.LEFT_CONTROL, Keycode.ALT, Keycode.F)
    keyboard.release_all()
    
#Making while loop to make all things work together
    
while(1):
    clkState = clk.value
    if(clk_last !=  clkState):
        if(dt.value != clkState):
            cw()
        else:
            ccw()
    if (sw.value == 0):
        pressTime = millis()
        time.sleep(0.2)
        longPress = False
        while(sw.value == 0):
            if(millis() - pressTime > 1000 and not longPress):
                print("longPress")
                longPress = True
                long_press()
                
 
        if (not longPress):
            currentMode += 1
            currentMode %= totalMode
            print("Mode: " + str(currentMode))
            
    clk_last = clkState