import cv2
from PIL import Image
import io
import base64
camera = cv2.VideoCapture(0)

def getFrame():
    ret, frame = camera.read()
    if not ret:
            print("Errore: frame non trovato\n")
    
    RGBframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return RGBframe

def encode64(frame):
    pil_img = Image.fromarray(frame)                        #Converto l'array rappresentante il frame RGB in immagine

    buffer = io.BytesIO()                                   #Creo il buffer di byte
    pil_img.save(buffer, format="PNG")                      #Salvo l'immagine in formato PNG nel buffer 
    img_bytes = buffer.getvalue()                           #Estraggo i bytes dell'immagine dal buffer

    img_b64 = base64.b64encode(img_bytes).decode("utf-8")   #Codifico i bytes in stringa ASCII (base 64)

    return img_b64

def camRelease():
      camera.release()