import json
import test2

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from qdas import db
from qdas.models import Survey, Responses
import os
import subprocess

APIKEY = "bHu1STJdEgOa12vLPoSeC1VzuvZvV22sigeRg93hixsF"
URL = "https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/81d71fa0-e15b-4f65-a075-f2115ab3354e"

authenticator = IAMAuthenticator(APIKEY)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(URL)

models = {
    "ar": "ar-MS_Telephony",
    "de": "de-DE_Telephony",
    "en": "en-US_Multimedia",
    "es": "es-ES_Telephony",
    "fr": "fr-FR_Multimedia"
    # "it": "it-IT_Telephony",
    # "ja": "ja-JP_Multimedia",
    # "ko": "ko-KR_Multimedia",
    # "nl": "nl-NL_Telephony",
    # "pt": "pt-BR_Telephony",
    # "zh": "zh-CN_Telephony"
}

def convertToText(tdir, survey_id=2):
    files = []
    for filename in os.listdir(tdir):
        if filename.endswith('.wav'):
            files.append(filename)
    files.sort()

    results = []
    
    fn_cut = files[0][:-4]
    lg = str(fn_cut[-2:])
 
    for filename in files:
        with open(tdir + filename, 'rb') as f:
            res = stt.recognize(audio=f, content_type='audio/wav', smart_formatting=True, model=models.get(lg),
                                inactivity_timeout=300).get_result()
            results.append(res)

    # print(results)

    text = []
    for file in results:
        record = []
        for result in file['results']:
            record.append(result['alternatives'][0]['transcript'].rstrip())
        full_sentence = (" ".join(record))
        text.append(full_sentence)
    print(f'text-->{text}')
    
    survey = db.session.query(Survey).order_by(Survey.id.desc()).get(survey_id)
    # if len(text) == nr_responses:
    responses = Responses(lan_code=lg, responses=text,
                              participant_folder=os.sep.join(os.path.normpath(tdir).split(os.sep)[-2:]))
    survey.response_ts.append(responses)
    print(survey.response_ts)
    db.session.commit()
    
    t_text = test2.translate(text, lg)
    print(t_text)
    test2.addResponseToDatabase(t_text, tdir)
    # else:
    #     print("Some of the responses are missing for this participant")
    # with open(dir + 'output.txt', 'w') as out:
    # out.writelines(text)


def loopDirs(rootdir='qdas/static/audioResponses', survey_id=2):
    paths = []
    survey_dir = db.session.query(Survey.survey_folder).filter(Survey.id == survey_id).scalar()
    print(f' dir -->{survey_dir}')
    for root, dirs, files in os.walk(rootdir + "/" + survey_dir):
        if not dirs:
            paths.append(root)

    folder_names = [responses.participant_folder for responses in Responses.query.all()]
    print(folder_names)

    for audioDir in paths:
        print(audioDir)
        if os.sep.join(os.path.normpath(audioDir).split(os.sep)[-2:]) in folder_names:
            print("these responses have been converted")
        else:
            print("convert")
            convertToText(audioDir + '/', survey_id=2)


def nrOfAudioResponses(rootdir, survey_id=2):
    survey_dir = db.session.query(Survey.survey_folder).filter(Survey.id == survey_id).scalar()
    nr_audio = len(next(os.walk(rootdir + "/" + survey_dir))[1])
    return nr_audio


loopDirs()
