import Movement as move
from MediaPipePE import searchPerson 
import vosk
import queue
import sounddevice as mic
import json

MODEL_PATH = "vosk-model-small-it-0.22" 
DEVICE_ID = 1 
SAMPLE_RATE = 44100
BLOCK_SIZE = 8000 

WAKEWORD_VARIANTS = [
    "soma",
    "somma",
    "zoma",
    "zomma",
    "ultrasoma",
    "ultra soma",
    "ultras soma",
    "ultras oma",
    "ultras home",
    "ultras hoc",
    "urne sono",
    "ultras ama",
    "ultras",
    "ultraso",
    "ultrasom",
    "ultrasomma",
    "ultrasomi",
    "ultrasomae",
    "ultrasuma",
    "ultrasona",
    "ultrazoma",
    "ultrassoma",
    "ultranoma",
    "ultraloma",
    "ultraroma",
    "tra soma",
    "trans ultrà soma",
    "ultra so",
    "ultra som",
    "ultra so ma",
    "ultra somma",
    "ultra sona",
    "ultra zoma",
    "ultra zona",
    "ultra suoma",
    "ultra suona",
    "ultra suona sono",
    "ultra stomaco",
    "ultra sole",
    "ultra soma eh",
    "ultra soma ok",
    "ok ultra soma",
    "hotel ultra soma",
    "hotel ultras",
    "hotel nuovo il trasimeno ultrà soma",
    "oltre soma",
    "oltresoma",
    "oltresona",
    "oltre sona",
    "oltre a roma",
    "oltre a soma",
    "oltre roma",
    "filtra soma",
    "multa sono",
    "multa soma",
    "ultras home",
    "a sono",
    "uova",
    "oltre a se home",
    "ultrasuoni",
    "ultrasuoni com",
    "uno tre soma"
]

audio_queue = queue.Queue() #Buffer audio per ricevere in streaming dal microfono

def Listen(command_queue, listeningEvent, wakewordEvent):
    def audio_callback(indata, frames, time, status):
        if listeningEvent.is_set():
            audio_queue.put(bytes(indata))
    model = vosk.Model(MODEL_PATH)
    device_info = mic.query_devices(DEVICE_ID, 'input')
    samplerate = int(device_info['default_samplerate'])
    recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
    # Stream audio
    with mic.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        dtype="int16",
        channels=1,
        device=DEVICE_ID,
        callback=audio_callback
    ):
        try:
            while True:
                data = audio_queue.get()

                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "")
                    #text = input("Inserisci: ")
                    if text:
                        print(text+"\n")
                        if wakewordEvent.is_set():
                            command_queue.put(text)
                            
                        else:
                            wakeFound = False
                            for i in text.split():
                                if i in WAKEWORD_VARIANTS:
                                    wakeFound = True
                            if text in WAKEWORD_VARIANTS or wakeFound:
                                wakewordEvent.set()
                                position = searchPerson()
                                while position != 0:
                                    if searchPerson() == 1:
                                        move.right()
                                        print("destra\n")
                                    elif searchPerson() == -1:
                                        move.left()
                                        print("sinistra\n")
                                    else:
                                        move.right()
                                    position = searchPerson()
                            
                            
                else:
                    partial = json.loads(recognizer.PartialResult())
                    text = partial.get("partial", "")

        except Exception as e:
            return "ERRORE"
