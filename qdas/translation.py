import json
import sqlite3
import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from qdas import db
from qdas.models import Questions, Survey, Responses

apikey = "yFuCchPFCVlie95N3m1FVetEvkCNlsj1Urt8hUVNTI0P"
url = "https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/d2b84c14-b9bb-4989-ae81-7fb1364906ba"

authenticator = IAMAuthenticator(apikey)
lt = LanguageTranslatorV3(version='2018-05-01', authenticator=authenticator)
lt.set_service_url(url)

lang_codes = ['ar', 'zh', 'nl', 'fr', 'de', 'it', 'ja', 'ko', 'pt', 'es']


# read from file
def read(rows):
    text = []
    for row in rows:
        questions = row[-1]
        [text.append(q) for q in json.loads(questions)]
        text.append(row[-2])
    return text


def translate(rows):
    text = read(rows)
    ts = []
    for lang in lang_codes:
        for sentence in text:
            translation = lt.translate(text=sentence, model_id='en-' + lang).get_result()
            ts.append(translation['translations'][0]['translation'].rstrip())
    print(ts)
    return ts


def identifySurveyLang(text):
    language = lt.identify(text).get_result()
    lcode = language['languages'][0]['language']
    return lcode


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def addToDatabase(t_text, question_count: int):
    l = 0
    t_chunks = list(chunks(t_text, question_count + 1))
    for chunk in t_chunks:
        survey = db.session.query(Survey).order_by(Survey.id.desc()).first()
        q_translated = Questions(lan_code=lang_codes[l], topic=chunk[-1], questions=chunk[:-1])
        survey.question_ts.append(q_translated)
        db.session.commit()
        l = l + 1

def translateResponse(text, lang):
    ts = []
    for sentence in text:
        translation = lt.translate(text=sentence, model_id=lang + '-en').get_result()
        ts.append(translation['translations'][0]['translation'].rstrip())
    print(ts)
    return ts

def addResponseToDatabase(t_text, tdir, survey_id):
    survey = db.session.query(Survey).order_by(Survey.id.desc()).get(survey_id)
    responses = Responses(lan_code="en", responses=t_text,
                              participant_folder=os.sep.join(os.path.normpath(tdir).split(os.sep)[-2:]))
    survey.response_ts.append(responses)
    db.session.commit()

if __name__ == "__main__":
    translate()
    addToDatabase()
    identifySurveyLang()
