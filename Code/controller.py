from sqlite3.dbapi2 import Error
import cv2
import face_recognition
import datetime
from face_recognition_models import cnn_face_detector_model_location
from numpy.core import machar
from numpy.core.records import array
import tensorflow.keras
import numpy as np
from PIL import Image, ImageOps, ImageTk
import db
import imutils

db.initialize()
model = tensorflow.keras.models.load_model("converted_keras\keras_model.h5")
color = (0,0,0)
text = ' '

def change_state(has_mask:bool, prediction:int):
    global color, text

    if  has_mask:
        text = 'Tiene cubrebocas ' + str(round(prediction*100,1)) + '%'
        color = (0, 255, 0)
    else:
        text = 'No tiene cubrebocas ' + str(round(prediction*100,1)) + '%'       
        color = (0,0,255)

def detect_mask(img_path: str):
    '''Detecta si el rostro reconocido está usando cubrebocas o no y devuelve 
       las predicciones
        
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

    mask_prediction = prediction[0][1]
    no_mask_prediction = prediction[0][0]

    if mask_prediction >=0.6:
        return True, mask_prediction

    return False, no_mask_prediction

def save_state(state: str):
    '''Registra el estado (con_mascara o sin_mascara) con fecha y hora'''
    try:
        date = str(datetime.datetime.now())
        db.save_state(state, date)
        print('Estado guardado en DB:', state, date)
    except:
        print('Ha ocurrido un error y no se ha podido guardar el estado en la BD')
    
def show_video():
    global cap, color, text
    face_locations = []   

    ret, frame = cap.read() 
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb)
    
    if face_locations:
        flag = datetime.datetime.now()
        for top, right, bottom, left in face_locations:          
            cv2.rectangle(frame, (left-15, top-35), (right+15, bottom+15), color, 3)
            cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)

    process_image(frame)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=640)
    im = Image.fromarray(frame)
    img = ImageTk.PhotoImage(image=im)
    return img

def capture():
    global cap
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

def release():
    cap.release()
    cv2.destroyAllWindows()

def process_image(frame: array):
    path = 'Code\imagenes\Frame.jpg'
    cv2.imwrite(path, frame)
    has_mask, percent = detect_mask(path)
    change_state(has_mask, percent)

    state = db.get_last_state()
    if state != None:
        prev_st, prev_time = state
        now = datetime.datetime.now()
        extra_time = prev_time + datetime.timedelta(seconds=20)
        
        if has_mask:
            act_state = 'con_mascara'
        else:
            act_state = 'sin_mascara' 

        if now > extra_time:
            save_state(act_state)
    else:
        save_state("init")

