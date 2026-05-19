import asyncio
import edge_tts
import pygame
import tempfile
import os
import sys

def speak(answer):
    asyncio.run(stream_tts(answer))

# SOLUZIONE PER WINDOWS: Corregge "RuntimeError: Event loop is closed"
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def stream_tts(text):
    voice = "it-IT-DiegoNeural"
    tts = edge_tts.Communicate(text, voice)

    # Creiamo un file temporaneo unico
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        filename = f.name

    try:
        # 1. Salviamo il file (il caricamento 'pezzo per pezzo' non è supportato bene da pygame)
        # Se il testo è lungo, questo è comunque quasi istantaneo.
        await tts.save(filename)

        # 2. Inizializziamo il mixer di pygame
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        # 3. IMPORTANTE: Aspettiamo che la musica finisca
        # Senza questo ciclo, lo script termina e chiude l'audio subito.
        print("Riproduzione in corso...")
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)

    finally:
        # Pulizia: chiudiamo il mixer e cancelliamo il file temporaneo
        pygame.mixer.quit()
        if os.path.exists(filename):
            os.remove(filename)


    