''' 
Lo scopo del programma è di far si che Ultrasoma "guardi" il soggetto con il quale sta parlando, segnalando il verso della 
rotazione da effettuare. 

Il programma, utilizzando la libreria mediapipe, legge i landmark relativi a spalle, fianchi e naso. 
Procede calcolando la media tra il punto medio di spalla sinistra con spalla destra e il punto medio di 
fianco sinistro con fianco destro, trovando il valore centrale del corpo inquadrato nella 
maniera più accurata possibile. 

Infine, ottenuta la posizione del centro del corpo, effettua dei micro-correggimenti, fino a quando il punto non
si troverà al centro del frame entro una certa tolleranza. E' importante notare che mediapipe restituisce la posizione 
dei landmark normalizzata in un valore compreso tra 0 e 1.0. (Es. 0 asse X -> estremo sinistro del frame, 1.0 asse X -> estremo destro del frame) 

'''
import time
import cv2
import mediapipe as mp

pose = mp.solutions.pose.Pose()
camera = cv2.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

show_landmarks = True

def draw_landmarks(frame, result, center, enable=True):
    if enable and result.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            result.pose_landmarks,
            mp.solutions.pose.POSE_CONNECTIONS,
            mp_drawing_styles.get_default_pose_landmarks_style()
        )
        h, w, _ = frame.shape
        center_px = int(center * w)
        center_py = h // 2      

        cv2.circle(frame, (center_px, center_py), 6, (0, 255, 0), -1)
        
        leftBoundX = int(0.40 * w)
        rightBoundX= int(0.60 * w)

        cv2.line(frame, (leftBoundX, 1), (leftBoundX, h), (0, 0, 255), 2)
        cv2.line(frame, (rightBoundX, 1), (rightBoundX, h), (0, 0, 255), 2)


        
try:
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(rgb_frame) 


        try:
            rightShoulder   = result.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]
            leftShoulder    = result.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
            rightHip        = result.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_HIP]
            leftHip         = result.pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_HIP]

            center = (                                                                                          #Calcolo della posizione del centro del corpo inquadrato lungo l'asse orizzontale del frame
                ((leftShoulder.x - rightShoulder.x)/2 + rightShoulder.x) + 
                ((leftHip.x - rightHip.x)/2 + rightHip.x)
            ) / 2

            draw_landmarks(frame, result, center, enable=show_landmarks)                                        #Disegno i landmark, il centro calcolato sull'asse orizzontale, e le rette che delimitano le aree di correzione

            print(f"Centro: {center}    ")

            if center < 0.40:
                print("Persona a sinistra! Correggo verso sinistra . . .") 
            elif center > 0.60:
                print("Persona a destra! Correggo verso destra . . .")
            else:
                print("Persona al centro . . .")

        except AttributeError:
            print("Nessuna persona rilevata . . .")

        cv2.imshow("Pose", frame)
        if cv2.waitKey(1) & 0xFF == 27:  
            break

except KeyboardInterrupt:
    print("Rilascio la camera . . .")
finally:
    camera.release()
    cv2.destroyAllWindows()