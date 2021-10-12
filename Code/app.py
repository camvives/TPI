import cv2
import face_recognition
import datetime
from face_recognition_models import cnn_face_detector_model_location
import tensorflow.keras
import numpy as np
from PIL import Image, ImageOps


cap = cv2.VideoCapture(0)
face_locations = []
flag_ant = datetime.datetime.now() - datetime.timedelta(minutes=1)
model = tensorflow.keras.models.load_model("converted_keras\keras_model.h5")
color = (0,0,0)
text = ''

def detect_mask(img_path: str):
    # Create the array of the right shape to feed into the keras model
    # The number of images you can put into the array is 1 in this case.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(img_path)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    global color, text
    mask_prediction = prediction[0][1]
    if  mask_prediction >= 0.5:
        text = 'Tiene cubrebocas ' + str(round(mask_prediction*100,1)) + '%'
        color = (0, 255, 0)
    else:
        text = 'No tiene cubrebocas ' + str(round(prediction[0][0]*100,1)) + '%'       
        color = (0,0,255)


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
        break
        