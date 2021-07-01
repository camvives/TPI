import face_recognition
import cv2
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

face_locations = []
face_encodings = []

video_capture = cv2.VideoCapture("Code\img\pexels-kampus-production-8348919.mp4") #Sin mascara
#video_capture = cv2.VideoCapture("Code\img\pexels-mikhail-nilov-7735486.mp4") #Con mascara
success, frame = video_capture.read()
cv2.imwrite("Code\imagenes\\frame_extraido.jpg", frame)

small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

face_locations = face_recognition.face_locations(small_frame)
face_encodings = face_recognition.face_encodings(small_frame, face_locations)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = tensorflow.keras.models.load_model("converted_keras\keras_model.h5")

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Replace this with the path to your image
image = Image.open("Code\imagenes\\frame_extraido.jpg")

#resize the image to a 224x224 with the same strategy as in TM2:
#resizing the image to be at least 224x224 and then cropping from the center
size = (224, 224)
image = ImageOps.fit(image, size, Image.ANTIALIAS)

#turn the image into a numpy array
image_array = np.asarray(image)

# Normalize the image
normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

# Load the image into the array
data[0] = normalized_image_array

# run the inference
prediction = model.predict(data)
print(prediction)

if prediction[0][0] < prediction[0][1]:
    color = (0, 255, 0)
else:
    color = (0,0,255)

for top, right, bottom, left in face_locations:
    cv2.rectangle(small_frame, (left-15, top-35), (right+15, bottom+15), color, 2)

cv2.imshow('Video', small_frame)
cv2.waitKey() 