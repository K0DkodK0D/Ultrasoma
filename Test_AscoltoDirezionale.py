from Microfono import Microfono

MIC_SX_ID = "Microfono (USB Microphone), MME"
MIC_DX_ID = "Microfono (2- USB Microphone), MME"

micSx = Microfono(MIC_SX_ID)
micDx = Microfono(MIC_DX_ID)

print(f"Sx: {micSx.mic_id}\nDx: {micDx.mic_id}")
#print(f"Mic sx: {getDecibels()}\n Mic dx: {getDecibels()}\n\n\n")
#print(f"Finito\n")