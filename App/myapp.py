# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 17:43:33 2021

@author: Chanuka Abeysinghe
"""

from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello World</h1>"

if __name__ =="__main__":
    app.run(debug=True)
