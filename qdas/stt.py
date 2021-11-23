import json
import os
import subprocess
import shutil
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from qdas import db, translation
from qdas.models import Survey, Responses



APIKEY = "1njZRQgYAuB2NBFFj2azPrFYdP2mLcaQtcBdkSPUaFlC"
URL = "https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/9c3ec9fa-b798-44f6-9f3d-67f8406f20a0/"

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

def convertToText(dir, survey_id):
    files = []
    for filename in os.listdir(dir):
        if filename.endswith('.wav'):
            files.append(filename)
    files.sort()

    results = []
    #get language from filename
    fn_cut = files[0][:-4]
    lg = str(fn_cut[-2:])
    print(lg)

    for filename in files:
        with open(dir + filename, 'rb') as f:
            try:
                res = stt.recognize(audio=f, content_type='audio/wav', smart_formatting=True, model=models.get(lg),
                                    inactivity_timeout=300).get_result()
                results.append(res)
            except ApiException as ex:
                print("Method failed with status code " + str(ex.code) + ": " + ex.message)

    text = []
    for file in results:
        record = []
        for result in file['results']:
            record.append(result['alternatives'][0]['transcript'].rstrip())
        full_sentence = (" ".join(record))
        text.append(full_sentence)
    survey = db.session.query(Survey).order_by(Survey.id.desc()).get(survey_id)
    # if len(text) == nr_responses:
    responses = Responses(lan_code=lg, responses=text,
                              participant_folder=os.sep.join(os.path.normpath(dir).split(os.sep)[-2:]))
    survey.response_ts.append(responses)
    db.session.commit()

    if lg != "en":
        # translate
        t_text = translation.translateResponse(text, lg)
        translation.addResponseToDatabase(t_text, dir, survey_id)

def loopDirs(rootdir, survey_id):
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
        elif len(os.listdir(audioDir)) == 0:
            print("Directory is empty")
            shutil.rmtree(audioDir)
        else:
            print("convert")
            convertToText(audioDir + '/', survey_id)


def nrOfAudioResponses(rootdir, survey_id):
    survey_dir = db.session.query(Survey.survey_folder).filter(Survey.id == survey_id).scalar()
    nr_audio = len(next(os.walk(rootdir + "/" + survey_dir))[1])
    return nr_audio


if __name__ == "__main__":
    loopDirs()
    convertToText()
