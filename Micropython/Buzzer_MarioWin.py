from machine import Pin, PWM
import time

#Configuracion de salida pwm y entrada el boton
buzzer = PWM(Pin(18))
buzzer.duty(0)  #Inciamos con el buzzer en silencio
button = Pin(12, Pin.IN, Pin.PULL_UP)

#Definición de la frecuencia de cada una de las notas musicales
G3=196; C4=261; E4=329; G4=392; C5=523; E5=659; G5=784
GS3=208; DS4=311; GS4=415; DS5=622; GS5=831
AS3=233; D4=294; F4=349; AS4=466; D5=587; F5=698; AS5=932; C6=1046

#Melodia de victoria de Mario
#Lista de tuplas con la tupla ahorramos memoria (Frecuencia, Duracion)
mario_win_slow = [
    # Arpegio 1 (Do Mayor)
    (G3, 0.12), (C4, 0.12), (E4, 0.12), (G4, 0.12), (C5, 0.12), (E5, 0.12), (G5, 0.3), (E5, 0.3),
    (0, 0.1),
    # Arpegio 2 (Lab Mayor)
    (GS3, 0.12), (C4, 0.12), (DS4, 0.12), (GS4, 0.12), (C5, 0.12), (DS5, 0.12), (GS5, 0.3), (DS5, 0.3),
    (0, 0.1),
    # Arpegio 3 (Sib Mayor)
    (AS3, 0.12), (D4, 0.12), (F4, 0.12), (AS4, 0.12), (D5, 0.12), (F5, 0.12), (AS5, 0.3),
    # Fanfarria final
    (AS5, 0.16), (AS5, 0.16), (AS5, 0.16), (C6, 1.0)
]

def play_note(freq, duration):
    """Reproduce la nota con timbre cuadrado de 8 bits."""
    if freq == 0: #Quiero silencio
        buzzer.duty(0)#0V constantes
    else:
        buzzer.freq(freq)
        # Duty al 50% para el sonido retro
        buzzer.duty(512) 
    
    time.sleep(duration) #Mantiene el sonido por el tiempo exacto necesitado
    buzzer.duty(0)
    time.sleep(0.04) # Silencio para separar notas

print("Modo lento activado en Pin 12. ¡Presiona para ganar!")

while True:
    if button.value() == 0:
        print("¡Victoria pausada! 🚩")
        
        for note, duration in mario_win_slow:
            play_note(note, duration)
            
        time.sleep(1) # Seguridad para el pulsador (No rebote)