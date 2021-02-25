# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 17:43:33 2021

@author: Chanuka Abeysinghe
"""

from flask import Flask,render_template,request
import pickle
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('healthy_lung.html')

if __name__ =="__main__":
    app.run(debug=True)
