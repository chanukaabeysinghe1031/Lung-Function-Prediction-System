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
from passlib.hash import sha256_crypt


# *********************************************VARIABLES**********************************************************
UPLOAD_FOLDER = r"./static"
MODEL_PATH = "D:\IIT\4th year\FYP\Lung Fibrosis\Prototype\Lung-Function-Prediction-System\App\my_model.h5"

# *****************************************DEFINE FLASK APP*******************************************************
app = Flask(__name__)

# ***********************************CONFIGURING TH MYSQL DATABASE************************************************
app.config['MYSQL_HOST']            = 'localhost'
app.config['MYSQL_USER']            = 'root'
app.config['MYSQL_PASSWORD']        = ''
app.config['MYSQL_DB']              = 'HealthyLung'
app.config['MYSQL_CURSORCLASS']     = 'DictCursor'

mysql = MySQL(app)
# ______________________________________________________________________________
#                                   LOAD MODEL
# ______________________________________________________________________________


def load_model():
    global model
    model = tf.keras.models.load_model('model.h5')
    print(" * Model loaded!")


# _______________________________________________________________________________
#                                 PREPROCESS DATA
# _______________________________________________________________________________

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
# _______________________________________________________________________________
#                                      ROUTES
# _______________________________________________________________________________


#                      HOME ROUTE
@app.route('/')
def home():
    return render_template("home.html")

#                      REGISTER


@app.route("/register", methods=["Get","Post"])
def registerDoctor():
    if request.method=='GET':
        return render_template("register.html")
    else:
        # Get data from the register form
        firstName = request.form['firstName']
        secondName = request.form['secondName']
        userName = request.form['userName']
        password = request.form['password']

        # Hashing the password
        hashed_password = sha256_crypt.encrypt(password)

        # Connection to the database
        cursor=mysql.connection.cursor()

        sql = "INSERT INTO doctors VALUES (%s, %s, %s, %s)"
        values = (firstName,secondName,userName,hashed_password)
        cursor.execute(sql, values)

        mysql.connection.commit()

        # Save the data in the session
        session['firstName'] = firstName
        session['secondName'] = secondName
        session['userName'] =userName

        # Load Model
        print("LOADING MODEL")
        load_model()
        print("MODEL LOADED SUCCESSFULLY")

        return redirect(url_for("home"))


#                        LOGIN
@app.route("/login", methods=["Get","Post"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        # Get the data from the login form
        userName = request.form['userName']
        password = request.form['password']

        # Get the user from the sql database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT *FROM doctors WHERE username=%s", (userName,))
        user = cursor.fetchone()

        # check whether there is a user with the username entered
        if len(user)>0 :
            # Check whether the input password and the password from the database similar
            if sha256_crypt.verify(password,user['password']):
                # Save data in the session
                session['firstName'] = user['firstName']
                session['secondName'] = user['secondName']
                session['userName'] = user['username']

                # Load Model
                print("LOADING MODEL")
                load_model()
                print("MODEL LOADED SUCCESSFULLY")
                return redirect(url_for("home"))
            else :
                return redirect(url_for("login"))
        else :
            return redirect(url_for("login"))


#                     PREDICT
@app.route("/predict", methods=["Get", "Post"])
def predict():
    if request.method == "POST":
        
        image= request.files["image"]
        basepath=os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, '', secure_filename(image.filename)
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
            return render_template("home.html", prediction=prediction[0][0])
    return render_template("home.html", prediction=0)


#                           LOGOUT
@app.route("/logout", methods=["Get", "Post"])
def logout():
    session.clear()
    return render_template("login.html")
# ______________________________________________________________________________


if __name__ == "__main__":
    app.secret_key = "0779302236199710311231231231234"
    app.run(port=12000, debug=True)
