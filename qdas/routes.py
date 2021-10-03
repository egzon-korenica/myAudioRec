import os
import sqlite3
from qdas import app, tts, translation, db
from flask import request, render_template, url_for, redirect
from qdas.forms import SurveyForm
from qdas.models import Questions


@app.route("/")
def home():
        return render_template("homepage.html")

@app.route("/audio", methods=['POST', 'GET'])
def index():
    questions = Questions.query.all()
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')
        return render_template('response.html', request="POST", questions = questions)
    else:
        return render_template("response.html", questions = questions)


@app.route('/background_process_test')
def background_process_test():
    tts.readQuestion()
    #tts.readQuestion1("de")
    return ("nothing")

@app.route('/lt_process')
def translate():
    translation.translate()
    return ("nothing")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    questions = Questions.query.all()
    return render_template("dashboard.html", questions = questions)

def rows():
    conn = sqlite3.connect('qdas/site.db')
    print("Opened database successfully");
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(date_posted), id, q1, q2, q3 FROM Questions")
    rows = cursor.fetchall()
    return rows

@app.route("/dashboard/create-survey", methods=["GET", "POST"])
def create_survey():
    form = SurveyForm()
    if form.validate_on_submit():
        questions = Questions(q1=form.q1.data, q2=form.q2.data, q3=form.q3.data)
        db.session.add(questions)
        db.session.commit()
        text = rows()
        tts.readQuestion(text)
        translation.translate(text)
        return redirect(url_for('dashboard'))
    return render_template("create_survey.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
