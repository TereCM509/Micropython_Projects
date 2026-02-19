"""
Engr. Teresa Cortes Magallon
Buzzer Control
02/01/2026
"""
#Importar modulos
from machine import Pin, PWM
import time

# Configuración del Buzzer en Pin 18
# Usamos duty(0) para que no empiece sonando solo
buzzer = PWM(Pin(18))
buzzer.duty(0) 

# Configuración del Botón en Pin 19
button = Pin(19, Pin.IN, Pin.PULL_UP)

def play_sound(frequency, duration):
    buzzer.freq(frequency)
    buzzer.duty(512)      # 50% de ciclo de trabajo
    time.sleep(duration)
    buzzer.duty(0)        # Apagar el sonido tras la duración

while True:
    # Si el valor es 0, significa que el botón fue presionado
    if button.value() == 0:
        for i in range(2):
            play_sound(440, 0.6) # Nota La (A4)
            play_sound(900, 0.6) # Nota más aguda
    
    time.sleep(0.1) # Pequeña pausa para estabilidad del procesador
