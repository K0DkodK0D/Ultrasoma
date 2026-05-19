import serial
from Audio import speak

try:
    Arduino = serial.Serial(port='COM4', baudrate=9600, timeout=5)
    speak("Connessione alle periferiche riuscita.")
except serial.SerialException:
    speak("Nessun dispositivo seriale trovato. Modalità test attiva.")
    Arduino = None

def readDistance():
    return Arduino.readline().decode("utf-8").strip()

def send(comando):
    Arduino.write((chr(ord('a')+comando).encode("utf-8")))
