# Install dependencies
# authenticate
# convert a string
# convert fromm a file
# using new language models
import json

url = 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/026c799e-4fe9-4f51-9666-cd48b628ec99'
apikey = 'YFtxheQpnYkOLztffr02FHIyCTmMXFo3pNhwO2mZ2QKn'

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
import playsound
import sqlite3
from qdas import db
from qdas.models import Questions, Survey

# setup service
authenticator = IAMAuthenticator(apikey)
# new tts service
tts = TextToSpeechV1(authenticator=authenticator)
# set service url
tts.set_service_url(url)

voices = {
    "ar": "ar-AR_OmarVoice",
    "de": "de-DE_BirgitV3Voice",
    "en": "en-GB_KateV3Voice",
    "es": "es-ES_EnriqueV3Voice",
    "fr": "fr-CA_LouiseV3Voice"
    "it": "it-IT_FrancescaV3Voice",
    # "ja": "ja-JP_EmiV3Voice",
    # "ko": "ko-KR_HyunjunVoice",
    # "nl": "nl-BE_AdeleVoice",
    # "pt": "pt-BR_IsabelaV3Voice",
    # "zh": "zh-CN_LiNaVoice"
}

# create interview folder

def audioDir():
    i = 1
    keepGoing = True
    while keepGoing:
        path = "qdas/static/audios/survey_{:03d}/".format(i)
        if not os.path.exists(path):
            os.makedirs(os.path.dirname("qdas/static/audios/survey_{:03d}/".format(i)), exist_ok=False)
            keepGoing = False
        i += 1


def read(lcode, survey_id):
    surveyQuestions = db.session.query(Questions).filter(Questions.survey_id == survey_id,
                                                         Questions.lan_code == lcode).all()
    text = []
    for questions in surveyQuestions:
        for q in questions.questions:
            text.append(q)

    return text


def readQuestion(lcode, voice, dir, survey_id):
    text = read(lcode, survey_id)
    ctr = 0
    for sentence in text:
        with open(dir + lcode + '{ctr:02d}.mp3'.format(ctr=ctr), 'wb') as audio_file:
            res = tts.synthesize(sentence, accept='audio/mp3', voice=voice).get_result()
            audio_file.write(res.content)
            ctr += 1


def createAudioFiles(dir, survey_id):
    for key, value in voices.items():
        readQuestion(key, value, dir, survey_id)


if __name__ == "__main__":
    read()
    readQuestion()
    createAudioFiles()
    audioDir()
