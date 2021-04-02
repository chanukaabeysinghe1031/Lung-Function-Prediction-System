from flask import Flask
from flask import render_template
from flask import request
import os

UPLOAD_FOLDER = "/Users/chanukaabeysinghe/Desktop/FYP/Lung-Function-Prediction-System/App/static"
app = Flask(__name__)
@app.route("/", methods=["Get","Post"])

def predict():
    if request.method == "POST":
        image= request.files["image"]
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