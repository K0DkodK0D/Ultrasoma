import serial

Arduino = serial.Serial(port='COM4', baudrate=9600, timeout=1)

def send(comando):
    Arduino.write(comando.encode())
