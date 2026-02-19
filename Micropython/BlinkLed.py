import machine
import time

pinLed = machine.Pin(2, machine.Pin.OUT)

while True:
    pinLed.value(1)
    print("Prendido")
    time.sleep(1)
    
    pinLed.value(0)
    print("Apagado")
    time.sleep(1)