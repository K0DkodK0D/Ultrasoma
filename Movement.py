import SerialCommunication as Arduino
from enum import Enum
import random
import json
import time

class Movements(Enum):
    Forward = 0
    Left = 1
    Right = 2
    Backwards = 3
    Stop = 4

def forward():
    Arduino.send(Movements.Forward)
    print("Forward . . .\n")
def left():
    Arduino.send(Movements.Left)
    print("Left . . .\n")
def right():
    Arduino.send(Movements.Right)
    print("Right . . .\n")
def backwards():
    Arduino.send(Movements.Backwards)
    print("Backwards . . .\n")
def stop():
    Arduino.send(Movements.Stop)
    print("Stop . . .\n")
    


def idle(listeningEvent, wakewordEvent):
    while True:
        movement = random.randint(0, 4)
        duration = random.randint(2, 9)
        #if checkDistances(movement):
        Arduino.send(movement)
        print(f"Idling: {movement} for {duration} seconds\n")
        startTime = time.time()
        while time.time() < (startTime + duration):
            if wakewordEvent.is_set():
                stop()
            while wakewordEvent.is_set():
                continue




        #print("Obstacle ahead!\n")

def Line():
    print("Following line . . .")