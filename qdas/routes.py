import os
import glob
import sqlite3
import json
import shutil
from random import randint
from qdas import app, tts, translation, db, querys, response, stt, toneAnalysis, nlu
from flask import request, render_template, url_for, redirect, jsonify
from qdas import progress_elements
from qdas.forms import SurveyForm
from qdas.models import Questions, Survey, Responses
from datetime import datetime
from qdas.progress_elements import PROGRESSES, convert, create


@app.route("/<int:survey_id>")
def home(survey_id):
    return render_template("homepage.html", survey_id=survey_id)


@app.route("/<int:survey_id>/index", methods=['POST', 'GET'])
def index(survey_id):
    lang = request.args.get('language')
    questions = tts.read(lang, survey_id)
    print(questions)
    post_url = request.path
    topic = db.session.query(Questions.topic).filter(Questions.survey_id == survey_id,
                                                     Questions.lan_code == lang).first()

    survey = Survey.query.get(survey_id)
    print(survey)
    sf = survey.survey_folder

    tdir = (str(max(glob.glob(os.path.join('qdas/static/audios', '*/')), key=os.path.getmtime))[:-1] + "/").replace(
        "qdas", ".")
    if request.method == "POST":
        lg = str(request.referrer)[-2:]
        response.saveResponse(lg, sf)
        return render_template('index.html', request="POST", questions=questions, topic=topic, dir=tdir, post_url=post_url)
    else:
        response.audioResponseDir(sf)
        return render_template("index.html", questions=questions, topic=topic, dir=tdir, post_url=post_url)


@app.route('/background_process_test')
def background_process_test():
    # tts.readQuestion()
    # tts.readQuestion1("de")
    return ("nothing")


@app.route('/lt_process')
def translate():
    translation.translate()
    return ("nothing")

@app.route("/", methods=["GET", "POST"])
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


@app.route("/dashboard/create-survey/check/<int:checkerID>", methods=["GET"])
def check_create_status(checkerID):
    if checkerID not in PROGRESSES:
        return("-1")
    else:
        return(f"{PROGRESSES[checkerID].step}")


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
        id = randint(0, 10000)
        while id in PROGRESSES:
            id = randint(0, 10000)
        t = create(form.topic.data, questions_data, i, id)
        PROGRESSES[id] = t
        t.start()
        return f"{id}"
    return render_template("create_survey.html", form=form)


@app.route("/dashboard/delete/<int:survey_id>/<survey_folder>", methods=["POST"])
def delete_survey(survey_id, survey_folder):
    survey = Survey.query.get_or_404(survey_id)
    db.session.delete(survey)
    db.session.commit()
    shutil.rmtree('qdas/static/audios/' + survey_folder, ignore_errors=True)
    shutil.rmtree('qdas/static/audioResponses/' +
                  survey_folder, ignore_errors=True)
    return redirect(url_for('dashboard'))


@app.route("/dashboard/survey/<int:survey_id>/convert", methods=["POST"])
def converSurvey(survey_id):
    id = randint(0, 10000)
    while id in PROGRESSES:
        id = randint(0, 10000)
    t = convert(survey_id, "qdas/static/audioResponses", id)
    PROGRESSES[id] = t
    t.start()
    return(json.dumps({"id": id, "todos": t.steps}))


@app.route("/progress/<int:progress_id>", methods=["GET"])
def progress(progress_id):
    if progress_id not in PROGRESSES:
        return("-1")
    else:
        return(f"{PROGRESSES[progress_id].progress}")


@app.route("/dashboard/survey/<int:survey_id>", methods=["GET"])
def survey(survey_id):
    survey = db.session.query(Survey, Questions).join(Survey).filter(Survey.id == survey_id).filter(
        Questions.lan_code == "en").all()
    rootDir = 'qdas/static/audioResponses'
    nr_responses = db.session.query(Survey, Responses).join(Responses).filter(Survey.id == survey_id).filter(
        Responses.lan_code == "en").count()
    print(nr_responses)
    ta_data = toneAnalysis.getToneAnalysisResults(survey_id)
    #k_data = nlu.getFrequentKeywords(survey_id)
    #overall_data = nlu.getOverallKA(survey_id)
    nr_participants = stt.nrOfAudioResponses(rootDir, survey_id)
    nr_convLeft = nr_participants - nr_responses
    return render_template('survey.html', survey=survey, ta_data=ta_data,
                           nr_responses=nr_responses, nr_convLeft=nr_convLeft)


@app.route("/dashboard/survey/<int:survey_id>/responses", methods=["GET"])
def responses(survey_id):
    kws = nlu.getKeywordEmotion(survey_id)
    responses = db.session.query(Survey, Responses).join(
        Responses).filter(Survey.id == survey_id).all()

    cleaned_responses = []

    for r in responses:
        resp = r.Responses.__dict__
        folder_already_added = False
        for alre_resp in cleaned_responses:
            if alre_resp["folder"] == resp["participant_folder"]:
                if alre_resp["lang"] == "en":
                    alre_resp["lang"] = resp["lan_code"]
                for i, respText in enumerate(resp["responses"]):
                    alre_resp["responses"][i][resp["lan_code"]] = respText
                folder_already_added = True
                break
        if not folder_already_added:
            cleaned_responses.append(
                {"sid": resp["survey_id"], "rid": resp["id"], "folder": resp["participant_folder"], "lang": resp["lan_code"], "responses": [{"index": i, resp['lan_code']: r} for i, r in enumerate(resp["responses"])]})

    return render_template('responses.html', responses=cleaned_responses, kws=kws, survey_id=survey_id)


@app.route("/dashboard/survey/<int:survey_id>/responses/delete/<int:r_id>/<participant_folder>", methods=["POST"])
def delete_response(survey_id, r_id, participant_folder):
    response = Responses.query.get_or_404(r_id)
    db.session.delete(response)
    db.session.commit()
    pfolder = participant_folder.replace("-", "/")
    querys.deleteRes(pfolder)
    shutil.rmtree('qdas/static/audioResponses/' + pfolder, ignore_errors=True)
    if request.method == 'POST':
        return redirect(url_for('responses', survey_id=survey_id))


@app.route("/dashboard/survey/<int:survey_id>/keywords")
def keywords(survey_id):
    survey = db.session.query(Survey, Questions).join(Survey).filter(Survey.id == survey_id).filter(
        Questions.lan_code == "en").all()
    k_data = nlu.getFrequentKeywords(survey_id)
    overall_data = nlu.getOverallKA(survey_id)
    ent_data = nlu.getEntities(survey_id)
    entities_dict = {}
    for key, value in ent_data.items():
        entities_dict[key] = list(set(value))

    return render_template('keywords.html', survey=survey, k_data=k_data, overall_data=overall_data,
                           entities_dict=entities_dict, survey_id=survey_id)


# changed
@app.route("/dashboard/survey/<int:survey_id>/concepts")
def concepts(survey_id):
    c_data = nlu.getConcepts(survey_id)
    rel_data = nlu.getRelations(survey_id)
    return render_template('concepts.html', c_data=c_data, rel_data=rel_data, survey_id=survey_id)


if __name__ == "__main__":
    app.run(debug=True,
            host='127.0.0.1',
            port=5000,
            threaded=True)
