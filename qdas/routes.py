import os
import glob
import sqlite3
from qdas import app, tts, translation, db, querys
from flask import request, render_template, url_for, redirect
from qdas.forms import SurveyForm
from qdas.models import Questions, Survey
from datetime import datetime

@app.route("/")
def home():
        return render_template("homepage.html")

@app.route("/response", methods=['POST', 'GET'])
def index():
    lang = request.args.get('language')
    questions = tts.read(lang)
    currentSurvey = db.session.query(Survey).order_by(Survey.id.desc()).first()
    topic= db.session.query(Questions.topic).filter(Questions.survey_id == currentSurvey.id, Questions.lan_code == lang).first()
    tdir = (str(max(glob.glob(os.path.join('qdas/static/audios', '*/')), key=os.path.getmtime))[:-1] + "/").replace("qdas", ".")
    if request.method == "POST":
        f = request.files['audio_data']
        with open('audio.wav', 'wb') as audio:
            f.save(audio)
        print('file uploaded successfully')
        return render_template('response.html', request="POST", questions=questions, topic=topic, dir=tdir)
    else:
        return render_template("response.html", questions=questions, topic=topic, dir=tdir)


@app.route('/background_process_test')
def background_process_test():
    #tts.readQuestion()
    #tts.readQuestion1("de")
    return ("nothing")

@app.route('/lt_process')
def translate():
    translation.translate()
    return ("nothing")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    surveys = db.session.query(Survey, Questions).filter(Questions.lan_code=="en").filter(Survey.id == Questions.survey_id).order_by(Survey.id.desc()).all()
    return render_template("dashboard.html", surveys = surveys)


@app.route("/dashboard/create-survey", methods=["GET", "POST"])
def create_survey():
    form = SurveyForm()
    if form.validate_on_submit():
        survey_lang = translation.identifySurveyLang(form.q1.data)
        questions = Questions(lan_code=survey_lang, topic=form.topic.data, q1=form.q1.data, q2=form.q2.data, q3=form.q3.data)
        survey = Survey(question_ts=[questions])
        db.session.add(survey)
        db.session.commit()
        text = querys.rows()
        t_text = translation.translate(text)
        translation.addToDatabase(t_text)
        tts.audioDir()
        TARGET_DIR = str(max(glob.glob(os.path.join('qdas/static/audios', '*/')), key=os.path.getmtime))[:-1] + "/"
        tts.createAudioFiles(TARGET_DIR)
        return redirect(url_for('dashboard'))
    return render_template("create_survey.html", form=form)

@app.route("/survey/<int:survey_id>")
def survey(survey_id):
    survey = db.session.query(Survey, Questions).join(Survey).filter(Survey.id == survey_id).filter(Questions.lan_code=="en").all()
    return render_template('survey.html', survey = survey)

if __name__ == "__main__":
    app.run(debug=True)
