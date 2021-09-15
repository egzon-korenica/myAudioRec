#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
import os
import tts

app = Flask(__name__)


@app.route("/")
def home():
        return render_template("homepage.html")

@app.route("/audio", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')

        return render_template('index.html', request="POST")
    else:
        return render_template("index.html")


@app.route('/background_process_test')
def background_process_test():
    tts.readQuestion()
    return ("nothing")



if __name__ == "__main__":
    app.run(debug=True)
