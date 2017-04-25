import RPi.GPIO as GPIO
import time
import requests
import random

#inicializar
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#pines
arrayBotones = [24,25,8]
arrayLeds = [15,18,23]
ldr = 14

#variables
hoy = "dia"

#entradas y salidas
for pin in arrayBotones:
    GPIO.setup(pin, GPIO.IN)
for pin in arrayLeds:
    GPIO.setup(pin, GPIO.OUT)

#peticion post para mandar el score
def score(value1):
    report = {}
    report["value1"] = value1
    requests.post("https://maker.ifttt.com/trigger/your_event/with/key/your_key", data=report)

#peticion post para mandar el estado del dia
def estadoDelDia(value1):
    report = {}
    report["value1"] = value1
    requests.post("https://maker.ifttt.com/trigger/your_event/with/key/your_key", data=report)

#calcular numero random
def nrandom():
    n = random.randint(0, 2)
    arreglo = [arrayLeds[n], arrayBotones[n]]
    return arreglo

#metodo para calcular la luz
def RCtime(RCpin):
    leer = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, False)
    time.sleep(0.1)

    GPIO.setup(RCpin, GPIO.IN)
    while (GPIO.input(RCpin) == False):
        leer += 1
    return leer

while True:
    estado = RCtime(ldr)
    print(estado)
    
    if estado < 500: #si es de dia
        if hoy == "dia":
            estadoDelDia(hoy)
            hoy = "noche"
            print("Es de dia")
    else: #si es de noche
        if hoy == "noche":
            estadoDelDia(hoy)
            hoy = "dia"
            print("Es de noche")
        
        #comienzan los 30 segundos de videojuego
        print("Comienza Minigame")
        
        #declaracion de variables
        puntos = 0
        num = nrandom()

        #primer vuelta
        GPIO.output(num[0], True)
        salida = 0
        estadoAnterior = 0
        
        for i in range(300): #300 x 0.1seg = 30seg = 0.5min
            
            #leer boton guardando un estado anterior
            estado = GPIO.input(num[1])
            if estado == 1 and estadoAnterior == 0:
                salida = 1 - salida
                time.sleep(0.03)
            estadoAnterior = estado

            if salida == 1:
                GPIO.output(num[0], False)
                puntos += 1
                print("Puntos: ",puntos)
                
                num = nrandom()
                GPIO.output(num[0], True)
            
            time.sleep(0.1)
            salida = 0
        
        score(puntos)
        
        #apagar leds
        for led in arrayLeds:
            GPIO.output(led, False)
        
        print("Termina minigame")

GPIO.cleanup() #limpiar GPIO
