from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import sqlite3

apikey = "yFuCchPFCVlie95N3m1FVetEvkCNlsj1Urt8hUVNTI0P"
url = "https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/d2b84c14-b9bb-4989-ae81-7fb1364906ba"

authenticator = IAMAuthenticator(apikey)
lt = LanguageTranslatorV3(version='2018-05-01', authenticator=authenticator)
lt.set_service_url(url)

# read from file
def read(rows):
    text = []
    for row in rows:
        text.append(row[-3])
        text.append(row[-2])
        text.append(row[-1])
    return text

def translate(rows):
    text = read(rows)
    ts = []
    lang = "de"
    for sentence in text:
        translation = lt.translate(text=sentence, model_id='en-' + lang).get_result()
        ts.append(translation['translations'][0]['translation'].rstrip() + '\n')

    with open("qdas/static/question/test-" + lang + ".txt", 'w') as out:
            out.writelines(ts)
