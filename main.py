#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
import os
import tts
import translation

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
    tts.readQuestion1()
    return ("nothing")

@app.route('/lt_process')
def translate():
    translation.translate()
    return ("nothing")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
        if request.method == "POST":
           # getting input with name = fname in HTML form
           question1 = request.form.get("q1")
           # getting input with name = lname in HTML form
           question2 = request.form.get("q2")
           with open('./static/question/test.txt', 'w') as f:
               f.write(question1 + "\n" + question2)
        return render_template("admin.html")


if __name__ == "__main__":
    app.run(debug=True)
