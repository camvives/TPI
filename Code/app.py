import cv2
import face_recognition
import datetime
from face_recognition_models import cnn_face_detector_model_location
import tensorflow.keras
import numpy as np
from PIL import Image, ImageOps
import os
import data

data.initialize()
cap = cv2.VideoCapture(0)
face_locations = []
flag_ant = datetime.datetime.now() - datetime.timedelta(minutes=1)
model = tensorflow.keras.models.load_model("converted_keras\keras_model.h5")
color = (0,0,0)
text = ''
est_ant = None


def detect_mask(img_path: str):
    '''Detecta si el rostro reconocido está usando cubrebocas o no, inicializa 
        el porcentaje de acierto y el color del rectangulo del ROI. Si el estado 
        cambia, registra el cambio en la base de datos.
        
        @img_path debe ser el path de una imagen que contenga un rostro detectado'''

    # Crear array del tamaño correcto para alimentar el modelo de keras
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(img_path)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    # Normalizar la imagen
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Cargar la imagen en el array
    data[0] = normalized_image_array

    # Correr el motor de inferencia
    prediction = model.predict(data)
    global color, text, est_ant

    mask_prediction = prediction[0][1]

    if  mask_prediction >= 0.5:
        text = 'Tiene cubrebocas ' + str(round(mask_prediction*100,1)) + '%'
        color = (0, 255, 0)

        if est_ant is False or est_ant is None:
            save_state('con_mascara')
            est_ant = True 
    else:
        text = 'No tiene cubrebocas ' + str(round(prediction[0][0]*100,1)) + '%'       
        color = (0,0,255)

        if est_ant or est_ant is None:
            save_state('sin_mascara')
            est_ant = False 


def save_state(state: str):
    '''Registra el estado (con_mascara o sin_mascara) con fecha y hora'''

    date = str(datetime.datetime.now())
    data.save_state(state, date)

    print('estado guardado en DB:', state, date) 


while True:
    ret, frame = cap.read() 
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb)
    
    if face_locations:
        flag = datetime.datetime.now()
        for top, right, bottom, left in face_locations:          
            cv2.rectangle(frame, (left-15, top-35), (right+15, bottom+15), color, 3)
            cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)

        time_change = datetime.timedelta(seconds=5)

        if flag > (flag_ant + time_change):   
            path = 'Code\imagenes\Frame.jpg'
            cv2.imwrite(path, frame)
            detect_mask(path)
            flag_ant = datetime.datetime.now()


    cv2.imshow('Mask Detector', frame)
    if cv2.waitKey(1) == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        os.remove('Code\imagenes\Frame.jpg')
        break
        
