from flask import Flask
from flask import render_template

app = Flask(__name__)
@app.route("/", methods=["Get","Post"])

def predict():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(port=12000,debug=True )