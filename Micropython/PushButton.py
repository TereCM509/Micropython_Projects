"""
Engr. Teresa Cortes Magallon
Push button - Pull Up
24/01/26
"""

from machine import Pin
import time
#Configuration: OUTPUT
Led1 = Pin(27, Pin.OUT)
Led2 = Pin(26, Pin.OUT)

#Initial State 
Led1.off()
Led2.off()

#Configuration: INPUT
pushButton1 = Pin(18, Pin.IN, Pin.PULL_UP) #PullUp always receiving 1 
pushButton2 = Pin(19, Pin.IN, Pin.PULL_UP)

while True:
    
    if pushButton1.value() == 0: #Si se presiona el boton go to GND
        Led1.toggle()   #Change state
        time.sleep(0.3) #Avoid Debouncing

        
    if pushButton2.value() == 0:
        Led2.toggle()
        time.sleep(0.3)
        

        


    