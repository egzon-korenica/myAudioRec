from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from qdas import db
from qdas.models import Survey, Responses
import os
import subprocess



APIKEY = "bHu1STJdEgOa12vLPoSeC1VzuvZvV22sigeRg93hixsF"
URL = "https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/81d71fa0-e15b-4f65-a075-f2115ab3354e"

authenticator = IAMAuthenticator(APIKEY)
stt = SpeechToTextV1(authenticator = authenticator)
stt.set_service_url(URL)

def convertToText(dir, survey_id):
    files = []
    for filename in os.listdir(dir):
        if filename.endswith('.wav'):
            files.append(filename)
    files.sort()

    results = []
    for filename in files:
        with open(dir + filename,'rb') as f:
            res = stt.recognize(audio=f, content_type='audio/wav', model='en-US_NarrowbandModel', inactivity_timeout=300).get_result()
            results.append(res)

    #print(results)

    text = []
    for file in results:
        record = []
        for result in file['results']:
            record.append(result['alternatives'][0]['transcript'].rstrip())
        full_sentence = (" ".join(record))
        text.append(full_sentence)

    print(text, len(text))

    survey = db.session.query(Survey).order_by(Survey.id.desc()).get(survey_id)
    if len(text) == 3:
        responses = Responses(lan_code="en", res1=text[0], res2=text[1], res3=text[2], participant_folder = os.sep.join(os.path.normpath(dir).split(os.sep)[-1:]))
        survey.response_ts.append(responses)
        db.session.commit()
    else:
        print("Some of the responses are missing for this participant")
    #with open(dir + 'output.txt', 'w') as out:
        #out.writelines(text)

def loopDirs(rootdir, survey_id):
    paths = []
    survey_dir = db.session.query(Survey.survey_folder).filter(Survey.id == survey_id).scalar()
    print(survey_dir)
    for root,dirs,files in os.walk(rootdir + "/" + survey_dir):
        if not dirs:
            paths.append(root)

    folder_names = [responses.participant_folder for responses in Responses.query.all()]
    print(folder_names)

    for audioDir in paths:
        if os.sep.join(os.path.normpath(audioDir).split(os.sep)[-1:]) in folder_names:
            print("these responses have been converted")
        else:
            convertToText(audioDir + '/', survey_id)


if __name__ == "__main__":
    loopDirs()
    convertToText()
