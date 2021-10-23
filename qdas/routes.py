import os
import glob
import sqlite3
import requests
from qdas import app, tts, translation, db, querys, response, stt
from flask import request, render_template, url_for, redirect
from qdas.forms import SurveyForm
from qdas.models import Questions, Survey, Responses
from datetime import datetime

@app.route("/")
def home():
        return render_template("homepage.html")

@app.route("/index", methods=['POST', 'GET'])
def index():
    #response.audioResponseDir()
    lang = request.args.get('language')
    questions = tts.read(lang)
    currentSurvey = db.session.query(Survey).order_by(Survey.id.desc()).first()
    topic= db.session.query(Questions.topic).filter(Questions.survey_id == currentSurvey.id, Questions.lan_code == lang).first()
    tdir = (str(max(glob.glob(os.path.join('qdas/static/audios', '*/')), key=os.path.getmtime))[:-1] + "/").replace("qdas", ".")
    if request.method == "POST":
        response.saveResponse()
        return render_template('index.html', request="POST", questions=questions, topic=topic, dir=tdir)
    else:
        response.audioResponseDir("audio")
        return render_template("index.html", questions=questions, topic=topic, dir=tdir)

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
        response.audioResponseDir("survey")
        sf = str(max(glob.glob(os.path.join('qdas/static/audioResponses/', '*/')), key=os.path.getmtime))[:-1]
        survey_folder =  os.sep.join(os.path.normpath(sf).split(os.sep)[-1:]) 
        survey = Survey(question_ts=[questions], survey_folder = survey_folder)
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

@app.route("/dashboard/survey/<int:survey_id>", methods = ["POST", "GET"])
def survey(survey_id):
    survey = db.session.query(Survey, Questions).join(Survey).filter(Survey.id == survey_id).filter(Questions.lan_code=="en").all()
    rootDir = 'qdas/static/audioResponses/'
    if request.method == "POST":
        stt.loopDirs(rootDir, survey_id)
        return redirect(url_for('survey', survey_id = survey_id))
    return render_template('survey.html', survey = survey)

@app.route("/dashboard/survey/<int:survey_id>/responses")
def responses(survey_id):
    responses = db.session.query(Survey, Responses).join(Responses).filter(Survey.id == survey_id).all()
    return render_template('responses.html', responses = responses)

if __name__ == "__main__":
    app.run(debug=True)
