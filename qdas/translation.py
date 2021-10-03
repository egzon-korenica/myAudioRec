import sqlite3
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from qdas import db
from qdas.models import QuestionsTranslated

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
        text.append(row[-3])
        text.append(row[-2])
        text.append(row[-1])
    return text

def translate(rows):
    text = read(rows)
    ts = []
    for lang in lang_codes:
        for sentence in text:
            translation = lt.translate(text=sentence, model_id='en-' + lang).get_result()
            ts.append(translation['translations'][0]['translation'].rstrip())
    return ts

def addToDatabase(t_text):
    conn = sqlite3.connect('qdas/site.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(date_posted), id FROM Questions")
    id = cursor.fetchall()

    l=0
    for i,k,s in zip(t_text[0::3], t_text[1::3], t_text[2::3]):
            q_translated = QuestionsTranslated(q_id=id[0][0], lan_code=lang_codes[l], q1=i, q2=k, q3=s)
            db.session.add(q_translated)
            db.session.commit()
            l=l+1
