from flask import Flask
from flask import render_template
from flask import request
import os
import sys
import os
import glob
import re
import numpy as np
import tensorflow as tf
from tensorflow import keras
from werkzeug.utils import secure_filename
#from keras.applications.imagenet_utils import preprocess_input, decode_predictions
#from keras.models import load_model
#from keras.preprocessing import image
import pydicom
import cv2

from flask import Flask 

UPLOAD_FOLDER = r"./static"

MODEL_PATH = "D:\IIT\4th year\FYP\Lung Fibrosis\Prototype\Lung-Function-Prediction-System\App\my_model.h5"

path =  ''

app = Flask(__name__)


def load_model():
    global model
    model = tf.keras.models.load_model('model.h5')
    print(" * Model loaded!")

def preprocess_data(image_location):
    print(image_location)
    ct_dicom = pydicom.read_file(image_location)
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



@app.route("/", methods=["Get","Post"])
def predict():
    print("LOADING MODEL")
    load_model()
    print("MODEL LOADED SUCCESSFULLY")
    if request.method == "POST":
        
        image= request.files["image"]
        basepath=os.path.dirname(__file__)
        file_path = os.path.join(
            basepath,'',secure_filename(image.filename)
        )
        if image:
            imageLocation = os.path.join(
                UPLOAD_FOLDER,
                image.filename
            )
            image.save(imageLocation)
            model_input=preprocess_data(imageLocation)
            prediction = model.predict(model_input).tolist()
            print(prediction)
            return render_template("index.html", prediction=prediction[0][0])
    return render_template("index.html",prediction=0)

if __name__ == "__main__":
    app.run(port=12000,debug=True )