import asyncio
import math
import numpy as np
import sounddevice as sd

SAMPLE_RATE = 44100
BLOCKSIZE = 1024
CHANNELS = 1

def rms(samples: np.ndarray) -> float:
    if samples.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(np.square(samples), axis=0)))

def rms_to_db(r: float, ref: float = 1.0, min_db: float = -120.0) -> float:
    if r <= 0:
        return min_db
    db = 20.0 * math.log10(r / ref)
    return max(db, min_db)

async def volume_consumer(queue: asyncio.Queue):
    max = -100
    c = 0
    while True:
        timestamp, db = await queue.get()
        if db > max:
            max = db
        print(f"{timestamp:.3f}s — {max:.1f} dBFS {c}")
        queue.task_done()
        c = c+1
        if c > 200:
            c = 0
            max = -100

def start_input_stream(queue: asyncio.Queue, loop: asyncio.AbstractEventLoop, micId):
    def callback(indata, frames, time, status):
        if status:
            print("Status:", status, flush=True)

        samples = np.mean(indata, axis=1) if indata.ndim > 1 else indata
        r = rms(samples)
        db = rms_to_db(r)
        timestamp = float(time.inputBufferAdcTime or time.currentTime or 0.0)

        loop.call_soon_threadsafe(queue.put_nowait, (timestamp, db))

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCKSIZE,
        dtype='float32',
        channels=CHANNELS,
        callback=callback,
        device=micId
    )
    stream.start()
    return stream

async def main():
    loop = asyncio.get_running_loop()
    queue = asyncio.Queue(maxsize=100)

    consumer_task = asyncio.create_task(volume_consumer(queue))

    print("Dispositivi disponibili:")
    for i, dev in enumerate(sd.query_devices()):
        print(i, dev['name'], f"(max input channels: {dev['max_input_channels']})")

    stream = start_input_stream(queue, loop, "Microfono (2- USB Microphone), MME")

    print("Monitoraggio volume avviato. Premi Ctrl+C per terminare.")

    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("\nTerminazione in corso…")
    finally:
        stream.stop()
        stream.close()
        consumer_task.cancel()
        await asyncio.gather(consumer_task, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())