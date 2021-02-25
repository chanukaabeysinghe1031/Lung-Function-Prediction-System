# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 22:20:39 2021

@author: Chanuka Abeysinghe
"""

import base64
import numpy as np
import io
from PIL import Image
import keras
from keras import backend as k
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from flask import request 
from flask import jsonify
from flask import Flask
import cv2

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>This is th flask backend for the severity of decline in lung function prediction system</h1>"

@app.route("/predict")
def predict():
    print(" Yes ")
    message = request.get_json(force=True)
    encoded= message['image']
    decoded =  base64.b64decode(encoded)
    image=Image.open(io.BytesIO(decoded))
    processedImage=preprocess(image)
    prediction = model.predict(processedImage).tolist()
    response = {
        'prediction':prediction[0]    
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run()

def getModel():
    global model 
    model=load_model('my_model.h5')
    print("*! Model loaded")
    
def preprocess(image):
    IMG_PX_SIZE = 50 
    NUMBER_OF_SLICES =10
    resized_images=[]
    resized_image=cv2.resize(np.array(image.pixel_array),(IMG_PX_SIZE,IMG_PX_SIZE))
    
    for singleImage in range(10):
        resized_images.append(resized_image)
    
    resized_images = np.transpose(resized_images, (1,2,0))
    
    return resized_images

print(" * Loading custom model")
getModel()


    

    
    
    
    
