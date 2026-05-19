from Movement import idle
from Interaction import Listen
from OpenAI_services import generateAnswer
from Audio import speak
from threading import Thread, Event
import queue
import time
#Main    : Establish connection with Arduino
#THREAD 1: Wait for wakeword -> Mic input on azure STT -> OpenAI API call -> Azure TTS output on speaker
#THREAD 2: Read distance values from Arduino -> Move accordingly (either following line or idling)
command_queue = queue.Queue()
listeningEvent = Event()
wakewordEvent = Event()
wakewordEvent.clear()
listeningEvent.set()

def AnswerHandler(listeningEvent, wakewordEvent):
    while True:
        text = command_queue.get()
        listeningEvent.clear()
        answer = generateAnswer(text)
        print(answer)
        speak(answer)

        time.sleep(2)
        listeningEvent.set()
        wakewordEvent.clear()


movement = Thread(target=idle, args=(listeningEvent, wakewordEvent))
listening = Thread(target=Listen, args=(command_queue, listeningEvent, wakewordEvent))       #Thread di ascolto da microfono
handler = Thread(target=AnswerHandler, args=(listeningEvent, wakewordEvent))

movement.start()
time.sleep(0.5)
listening.start()
time.sleep(0.5)
handler.start()

movement.join()
listening.join()
handler.join()
