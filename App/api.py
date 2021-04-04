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

#from keras.applications.imagenet_utils import preprocess_input, decode_predictions
#from keras.models import load_model
#from keras.preprocessing import image

from flask import Flask 

UPLOAD_FOLDER = "D:\IIT\4th year\FYP\Lung Fibrosis\Prototype\Lung-Function-Prediction-System\App\static"

MODEL_PATH = "D:\IIT\4th year\FYP\Lung Fibrosis\Prototype\Lung-Function-Prediction-System\App\my_model.h5"

model.load_model(MODEL_PATH)
model._make_predict_function()

app = Flask(__name__)
@app.route("/", methods=["Get","Post"])

def predict():
    if request.method == "POST":
        
        image= request.files["image"]
        basepath=os.path.dirname(__filr__)
        file_path = os.path.join(
            basepath,secure_filename    
        )
        if image:
            imageLocation = os.path.join(
                UPLOAD_FOLDER,
                image.filename
            )
            image.save(imageLocation )
            return render_template("index.html", prediction=1)
    return render_template("index.html",prediction=0)

if __name__ == "__main__":
    app.run(port=12000,debug=True )