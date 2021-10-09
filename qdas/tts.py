# Install dependencies
# authenticate
# convert a string
# convert fromm a file
# using new language models

url = 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/58f23641-330d-4584-a281-1fa87ff5431a'
apikey = 'EWtDUdU2pOw1TCVwiQtSPX7uSva3QSg8QBXzJpFX9Tbx'

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
import playsound
import sqlite3
from qdas import db
from qdas.models import Questions, Survey


# setup service
authenticator = IAMAuthenticator(apikey)
#new tts service
tts = TextToSpeechV1(authenticator=authenticator)
# set service url
tts.set_service_url(url)

#voices = ['ar-AR_OmarVoice', 'de-DE_BirgitV3Voice', 'en-GB_KateV3Voice', 'es-ES_EnriqueV3Voice', 'fr-CA_LouiseV3Voice',\
#'it-IT_FrancescaV3Voice', 'ja-JP_EmiV3Voice', 'ko-KR_SiWooVoice', 'nl-NL_EmmaVoice', 'pt-BR_IsabelaV3Voice', 'h-CN_ZhangJingVoice']

voices = {
  "ar": "ar-AR_OmarVoice",
  "de": "de-DE_BirgitV3Voice",
  "en": "en-GB_KateV3Voice",
  "es": "es-ES_EnriqueV3Voice",
  "fr": "fr-CA_LouiseV3Voice"
  #"it": "Mustang",
  #"ja": "Mustang",
  #"ko": "Mustang",
  #"nl": "Mustang",
  #"pt": "Mustang",
  #"de": "Mustang",
  #"zh": "Mustang"
}

# create interview folder

def audioDir():
    i=1
    keepGoing=True
    while keepGoing:
      path = "qdas/static/audios/audio_{}/".format(i)
      if not os.path.exists(path):
        os.makedirs(os.path.dirname("qdas/static/audios/audio_{}/".format(i)), exist_ok=False)
        keepGoing = False
      i += 1

def read(lcode):
    currentSurvey = db.session.query(Survey).order_by(Survey.id.desc()).first()
    surveyQuestions= db.session.query(Questions).filter(Questions.survey_id == currentSurvey.id, Questions.lan_code == lcode).all()
    text = []
    for question in surveyQuestions:
        text.append(question.q1)
        text.append(question.q2)
        text.append(question.q3)
    return text

def readQuestion(lcode, voice, dir):
    text = read(lcode)
    ctr = 0
    for sentence in text:
        with open(dir + lcode + '{ctr:02d}.mp3'.format(ctr=ctr), 'wb') as audio_file:
            res = tts.synthesize(sentence, accept='audio/mp3', voice=voice).get_result()
            audio_file.write(res.content)
            ctr +=1

def createAudioFiles(dir):
    for key, value in voices.items():
        readQuestion(key, value, dir)

if __name__ == "__main__":
    read()
    readQuestion()
    createAudioFiles()
    audioDir()
