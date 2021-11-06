import os
import glob
import sqlite3
import json
import shutil
from qdas import app, tts, translation, db, querys, response, stt, toneAnalysis, nlu
from flask import request, render_template, url_for, redirect, jsonify
from qdas.forms import SurveyForm
from qdas.models import Questions, Survey, Responses
from datetime import datetime


@app.route("/")
def home():
    return render_template("homepage.html")


@app.route("/index", methods=['POST', 'GET'])
def index():
    # response.audioResponseDir()
    lang = request.args.get('language')
    questions = tts.read(lang)
    currentSurvey = db.session.query(Survey).order_by(Survey.id.desc()).first()
    topic = db.session.query(Questions.topic).filter(Questions.survey_id == currentSurvey.id,
                                                     Questions.lan_code == lang).first()

    tdir = (str(max(glob.glob(os.path.join('qdas/static/audios', '*/')), key=os.path.getmtime))[:-1] + "/").replace(
        "qdas", ".")
    if request.method == "POST":
        lg = str(request.referrer)[-2:]
        response.saveResponse(lg)
        return render_template('index.html', request="POST", questions=questions, topic=topic, dir=tdir)
    else:
        response.audioResponseDir("audio")
        return render_template("index.html", questions=questions, topic=topic, dir=tdir)


@app.route('/background_process_test')
def background_process_test():
    # tts.readQuestion()
    # tts.readQuestion1("de")
    return ("nothing")


@app.route('/lt_process')
def translate():
    translation.translate()
    return ("nothing")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    page = request.args.get('page', 1, type=int)
    surveys = Survey.query \
        .join(Questions, Survey.id == Questions.survey_id) \
        .add_columns(Survey.id, Questions.topic, Questions.questions) \
        .filter(Survey.id == Questions.survey_id) \
        .filter(Questions.lan_code == "en") \
        .order_by(Survey.id.desc()) \
        .paginate(page=page, per_page=4)
    return render_template("dashboard.html", surveys=surveys)


@app.route("/dashboard/create-survey", methods=["GET", "POST"])
def create_survey():
    form = SurveyForm()
    form_data = {}
    i = 0
    for entry in form.questions.entries:
        q = entry.data
        form_data[f'question {str(i)}'] = q['question']
        i += 1
    if form.add_q.data:
        form.questions.append_entry({f"question {str(i)}": ""})
        return render_template("create_survey.html", form=form)
    if form.validate_on_submit():
        questions_data = [v for (k, v) in form_data.items() if 'question' in k]
        survey_lang = translation.identifySurveyLang(questions_data[0])
        questions = Questions(lan_code=survey_lang, topic=form.topic.data, questions=questions_data)
        response.audioResponseDir("survey")
        sf = str(max(glob.glob(os.path.join('qdas/static/audioResponses/', '*/')), key=os.path.getmtime))[:-1]
        survey_folder = os.sep.join(os.path.normpath(sf).split(os.sep)[-1:])
        survey = Survey(question_ts=[questions], survey_folder=survey_folder)
        db.session.add(survey)
        db.session.commit()
        text = querys.rows()
        t_text = translation.translate(text)
        translation.addToDatabase(t_text, i)
        tts.audioDir()
        TARGET_DIR = str(max(glob.glob(os.path.join('qdas/static/audios', '*/')), key=os.path.getmtime))[:-1] + "/"
        tts.createAudioFiles(TARGET_DIR)
        return redirect(url_for('dashboard'))
    return render_template("create_survey.html", form=form)


@app.route("/dashboard/delete/<int:survey_id>/<survey_folder>", methods=["POST"])
def delete_survey(survey_id, survey_folder):
    survey = Survey.query.get_or_404(survey_id)
    db.session.delete(survey)
    db.session.commit()
    shutil.rmtree('qdas/static/audios/' + survey_folder, ignore_errors=True)
    shutil.rmtree('qdas/static/audioResponses/' + survey_folder, ignore_errors=True)
    return redirect(url_for('dashboard'))


@app.route("/dashboard/survey/<int:survey_id>", methods=["POST", "GET"])
def survey(survey_id):
    survey = db.session.query(Survey, Questions).join(Survey).filter(Survey.id == survey_id).filter(
        Questions.lan_code == "en").all()
    rootDir = 'qdas/static/audioResponses'
    if request.method == "POST":
        stt.loopDirs(rootDir, survey_id)
        return redirect(url_for('survey', survey_id=survey_id))
    nr_responses = db.session.query(Survey, Responses).join(Responses).filter(Survey.id == survey_id).filter(
        Responses.lan_code == "en").count()
    print(nr_responses)
    ta_data = toneAnalysis.getToneAnalysisResults(survey_id)
    k_data = nlu.getFrequentKeywords(survey_id)
    overall_data = nlu.getOverallKA(survey_id)
    nr_participants = stt.nrOfAudioResponses(rootDir, survey_id)
    nr_convLeft = nr_participants - nr_responses
    return render_template('survey.html', survey=survey, ta_data=ta_data, \
                           k_data=k_data, nr_responses=nr_responses, nr_convLeft=nr_convLeft,
                           overall_data=overall_data)


@app.route("/dashboard/survey/<int:survey_id>/responses")
def responses(survey_id):
    kws = nlu.getKeywordEmotion(survey_id)
    responses = db.session.query(Survey, Responses).join(Responses).filter(Survey.id == survey_id).filter(
        Responses.lan_code == "en").all()

    return render_template('responses.html', responses=responses, kws=kws)


@app.route("/dashboard/survey/<int:survey_id>/keywords")
def keywords(survey_id):
    survey = db.session.query(Survey, Questions).join(Survey).filter(Survey.id == survey_id).filter(
        Questions.lan_code == "en").all()
    k_data = nlu.getFrequentKeywords(survey_id)
    overall_data = nlu.getOverallKA(survey_id)
    rel_data = nlu.getRelations(survey_id)
    print(rel_data)
    ent_data = nlu.getEntities(survey_id)
    entities_dict = {}
    for key, value in ent_data.items():
        entities_dict[key] = list(set(value))

    return render_template('keywords.html', survey=survey, k_data=k_data, overall_data=overall_data,\
     entities_dict=entities_dict, rel_data=rel_data)


if __name__ == "__main__":
    app.run(debug=True,
            host='127.0.0.1',
            port=5000,
            threaded=True)
