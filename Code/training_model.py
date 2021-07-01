from imutils import paths
import os
import numpy as np

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from sklearn.preprocessing import LabelBinarizer

dataset=r"C:\\Users\\camvi\Documents\Soporte\\TPI\\Mask Dataset"
imagePaths=list(paths.list_images(dataset))

data = []
labels = []

for im in imagePaths:
    label=im.split(os.path.sep)[-2]
    labels.append(label)
    image=load_img(im,target_size=(224,224))
    image=img_to_array(image)
    image=preprocess_input(image) #RGB a BGR
    data.append(image)

#Convierte los datos a arrays
data=np.array(data,dtype="float32")
labels=np.array(labels)

print(labels)