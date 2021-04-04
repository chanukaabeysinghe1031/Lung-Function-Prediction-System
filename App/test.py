import base64
import numpy as np
import io
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array
from flask import request
from flask import jsonify
from flask import Flask
import pydicom
import numpy as np
import cv2


app = Flask(__name__)
path =  './image.dcm'

def load_model():
    global model
    model = tf.keras.models.load_model('model.h5')
    print(" * Model loaded!")

def preprocess_data():
    ct_dicom = pydicom.read_file(path)
    img = ct_dicom.pixel_array
    resized_image=cv2.resize(np.array(ct_dicom.pixel_array),(50,50))
    image=np.array(resized_image)
    print(image.shape)
    input=[]
    for i in  range(10):
        input.append(image)

    input=np.array(input)
    resized_images = np.transpose(input, (1, 2, 0))

    print(resized_images.shape)
    input2=[]
    input2.append(resized_images)
    input2=np.array(input2)
    return input2


print(" * Loading Keras model...")
load_model()
testing_image=preprocess_data()
print(testing_image.shape)
prediction = model.predict(testing_image).tolist()
print(prediction)
