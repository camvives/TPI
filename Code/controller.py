from sqlite3.dbapi2 import Error
import cv2
import face_recognition
import datetime
from numpy.core.records import array
import tensorflow.keras
import numpy as np
from PIL import Image, ImageOps, ImageTk
import db
import imutils
import matplotlib.pyplot as plt

db.initialize()
model = tensorflow.keras.models.load_model("converted_keras\keras_model.h5")

def change_state(has_mask:bool, prediction:int):
    if has_mask:
        text = 'Tiene cubrebocas ' + str(round(prediction*100,1)) + '%'
        color = (0, 255, 0)
        return color, text

    text = 'No tiene cubrebocas ' + str(round(prediction*100,1)) + '%'       
    color = (0,0,255)
    return color, text

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
    try:
        global cap
        face_locations = []   

        _, frame = cap.read() 
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb)

        color, text = process_image(frame)

        if face_locations:
            for top, right, bottom, left in face_locations:          
                cv2.rectangle(frame, (left-15, top-35), (right+15, bottom+15), color, 3)
                cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = imutils.resize(frame, width=640)
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

        return img, color

    except:
        raise

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
    color, text = change_state(has_mask, percent)

    state = db.get_last_state()
    if state != None:
        prev_state, prev_time = state
        now = datetime.datetime.now()
        extra_time = prev_time + datetime.timedelta(seconds=30)
        extra_time_sm = prev_time + datetime.timedelta(seconds=5)
        
        if has_mask:
            act_state = 'con_mascara'
        else:
            act_state = 'sin_mascara' 

        stable_state_changed = (prev_state != has_mask) and (now > extra_time_sm)

        if now > extra_time or stable_state_changed:
            save_state(act_state)
    else:
        save_state("init")

    return color, text

def get_time():
    return datetime.datetime.now()

def get_session_data(start_time: datetime):
    data = db.get_session_data(start_time)
    
    with_mask = 0
    without_mask = 0

    for state in data:
        if state:
            with_mask += 1
        else: 
            without_mask += 1
    
    total = without_mask + with_mask

    return (with_mask, without_mask, total)


def get_month_data():
    month_data = db.get_month_data()

    count_with_mask = []
    count_without_mask = []
    days = []
    month_cases = []

    for data in month_data:
        day = data[1]
        days.append(int(day[8:10]))
        
    for i in range(32):
        day_cases = days.count(i)
        month_cases.append(day_cases)
    
    for day_cases in month_cases:
        day_data = month_data[:day_cases]
        
        with_mask = 0
        without_mask = 0

        for data in day_data:
            if data[0] == 'con_mascara':
                with_mask += 1
            if data[0] == 'sin_mascara':    
                without_mask += 1
        
        count_with_mask.append(with_mask)
        count_without_mask.append(without_mask)

        del month_data[:day_cases]
        
    days = list(set(days))
    
    cwm = []
    cwom = []

    for day in days:
        cwm.append(count_with_mask[day])
        cwom.append(count_without_mask[day])

    fig = plot_stats(days, cwm, cwom, "data_month")
    return fig
    
    

def plot_stats(days: list, count_with_mask: list, count_without_mask: list, file_name:str):
    x = np.arange(len(days))  # the label locations
    width = 0.35  # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot()
    rects1 = ax.bar(x - width/2, count_with_mask, width, label='Con Máscara', color='green')
    rects2 = ax.bar(x + width/2, count_without_mask, width, label='Sin Máscara', color='red')

    ax.set_ylabel('Cantidad de casos')
    ax.set_xticks(x)
    ax.set_xticklabels(days)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    fig.tight_layout()
    return fig