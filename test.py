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


# setup service
authenticator = IAMAuthenticator(apikey)
#new tts service
tts = TextToSpeechV1(authenticator=authenticator)
# set service url
tts.set_service_url(url)

voices = ['ar-AR_OmarVoice', 'de-DE_BirgitV3Voice', 'en-GB_KateV3Voice', 'es-ES_EnriqueV3Voice', 'fr-CA_LouiseV3Voice',\
'it-IT_FrancescaV3Voice', 'ja-JP_EmiV3Voice', 'ko-KR_SiWooVoice', 'nl-NL_EmmaVoice', 'pt-BR_IsabelaV3Voice', 'h-CN_ZhangJingVoice']

lang_codes = ['ar', 'zh', 'nl', 'fr', 'de', 'it', 'ja', 'ko', 'pt', 'es']

# create interview folder

def rows():
    conn = sqlite3.connect('qdas/site.db')
    print("Opened database successfully");
    cursor = conn.cursor()
    cursor.execute("SELECT lan_code, q1, q2, q3 FROM questions_translated")
    rows = cursor.fetchall()
    return rows
    
text = rows()

def interviewDir():
    i=1
    keepGoing=True
    while keepGoing:
      path = "interviews/interview_{}/".format(i)
      if not os.path.exists(path):
        os.makedirs(os.path.dirname("interviews/interview_{}/".format(i)), exist_ok=False)
        keepGoing = False
      i += 1

# read from db
def read(rows):
    text = []
    for row in rows:
        text.append(row[-3])
        text.append(row[-2])
        text.append(row[-1])
    return text
#text = ''.join(str(line) for line in text)


t_text = read(text)


def createAudio(t_text):
    for sentence in t_text:
        with open('qdas/static/audio/{ctr:02d}.mp3'.format(ctr=ctr), 'wb') as audio_file:
            res = tts.synthesize(sentence, accept='audio/mp3', voice='en-GB_JamesV3Voice').get_result()
            audio_file.write(res.content)
            ctr +=1

createAudio(t_text)




