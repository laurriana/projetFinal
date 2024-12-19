import busio
import board
import time
import pigpio
import threading

from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.ads1115 import P0
from adafruit_ads1x15.analog_in import AnalogIn
 
i2c = busio.I2C(board.SCL, board.SDA)
 
ads = ADS1115(i2c, 2/3)
data = AnalogIn(ads, P0)

pi = pigpio.pi()

SAVE = 16
BUZZ = 23
UNLOCK = 26
LED = 27
SERVO = 22

pi.set_mode(SAVE, pigpio.INPUT)
pi.set_pull_up_down(SAVE, pigpio.PUD_UP)


def creation_code():
    is_pressing_util_btn = not pi.read(SAVE)
    count = 0
    compteur = 0
    input_codes = []

    while len(input_codes) < 3:
        current_voltage = 0
        btn_state = pi.read(SAVE)
        if is_pressing_util_btn:
            if btn_state == 1:
                if count == 16:
                    is_pressing_util_btn = True
                    count = 0
                else:
                    count += 1
            else:
                if btn_state == 0:
                    if count == 16:
                        is_pressing_util_btn = False
                        compteur += 1
                        count = 0
                    else:
                        count += 1
                else:
                    count = 0 
        if pi.read(SAVE) == 0:
            current_voltage = int(data.voltage*10)
            input_codes.append(current_voltage)
            time.sleep(0.25)
            # block long presses 
    return input_codes

def read_button(event):
    while not event:
        print(int(data.voltage*10))
        time.sleep(0.08)

def enter_code():
    is_pressing_read_btn = not pi.read(UNLOCK)
    count = 0
    compteur = 0
    reading_codes = []

    while len(reading_codes) < 3:
        current_voltage = 0
        btn_state = pi.read(UNLOCK)
        if is_pressing_read_btn:
            if btn_state == 1:
                if count == 16:
                    is_pressing_read_btn = True
                    count = 0
                else:
                    count += 1
            else:
                if btn_state == 0:
                    if count == 16:
                        is_pressing_read_btn = False
                        compteur += 1
                        count = 0
                    else:
                        count += 1
                else:
                    count = 0 
        if pi.read(UNLOCK) == 0:
            current_voltage = int(data.voltage*10)
            reading_codes.append(current_voltage)
            time.sleep(0.25)
            # block long presses 
    return reading_codes

def compare_codes(enter_code, creation_code):
    try:
        if enter_code == creation_code:
            #code led
            for i in range(3):
                pi.write(LED, 1)
                time.sleep(0.5)
                pi.write(LED, 0)
                
            #code buzzer
            pi.write(23,1)
            time.sleep(1)
            pi.write(23,0)
            time.sleep(1)  

            #code matrice
            
            
            #code servo
            print("Vous avez entrez le bon code. Activation...")
            pi.set_PWM_dutycycle(SERVO, 2.5)
            time.sleep(2)
            pi.set_PWM_dutycycle(SERVO, 12.5)

        else :
            #code buzzer
            i = 0
            for i in range (5): 
                pi.write(23,1)
                time.sleep(0.3)
                pi.write(23,0)
                time.sleep(0.3)  
            #code matrice
            print("Vous avez entrez le mauvais code. Accès refusé.")
    except KeyboardInterrupt:
        print("au revoir!")
        

        # fermer le servo