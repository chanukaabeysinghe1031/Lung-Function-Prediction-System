from flask import Flask,url_for,session,redirect
from flask import render_template
from flask import request
import os
import numpy as np
import tensorflow as tf
from werkzeug.utils import secure_filename
import pydicom
import cv2
from flask_mysqldb import MySQL,MySQLdb
from flask import Flask
import bcrypt

#*********************************************VARIABLES**********************************************************
UPLOAD_FOLDER = r"./static"
MODEL_PATH = "D:\IIT\4th year\FYP\Lung Fibrosis\Prototype\Lung-Function-Prediction-System\App\my_model.h5"

#*****************************************DEFINE FLASK APP*******************************************************
app = Flask(__name__)

#***********************************CONFIGURING TH MYSQL DATABASE************************************************
app.config['MYSQL_HOST']            = 'localhost'
app.config['MYSQL_USER']            = 'root'
app.config['MYSQL_PASSWORD']        = ''
app.config['MYSQL_DB']              = 'HealthyLung'
app.config['MYSQL_CURSORCLASS']     = 'DictCursor'

mysql = MySQL(app)

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

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route("/register", methods=["Get","Post"])
def registerDoctor():
    if request.method=='GET':
        return render_template("register.html")
    else:
        firstName = request.form['firstName']
        secondName = request.form['secondName']
        userName = request.form['userName']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password,bcrypt.gensalt())

        cursor=mysql.connection.cursor()
        #cursor.execute("INSERT INTO doctors(firstName,secondName,username,password) values (%s,%s,%s.%s)",
                       #(firstName,secondName,userName,password))
        sql = "INSERT INTO doctors VALUES (%s, %s, %s, %s)"
        values = (firstName,secondName,userName,password)
        cursor.execute(sql, values)

        mysql.connection.commit()
        session['firstName'] = firstName
        session['secondName'] = secondName
        session['userName'] =userName
        return redirect(url_for("home"))

@app.route("/predict", methods=["Get","Post"])
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
    app.secret_key = "0779302236199710311231231231234"
    app.run(port=12000,debug=True )