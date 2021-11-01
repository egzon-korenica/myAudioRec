import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from qdas import db
from qdas.models import Survey, Responses



apikey = "KobRgKpaAwmvjjOmKoZIxPZcQ33f0Y3ap1Y_Rz3tX4e7"
url = "https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/372cbdb1-3eb7-4948-8390-c99205593cb7"

authenticator = IAMAuthenticator(apikey)
ta = ToneAnalyzerV3(version='2021-08-02', authenticator = authenticator)
ta.set_service_url(url)



def getToneAnalysis(survey_id):
    responses = db.session.query(Survey, Responses).join(Responses).filter(Survey.id == survey_id).all()
    r_texts = []
    for index, response in enumerate(responses):
        r_texts.append(response.Responses.res1)
        r_texts.append(response.Responses.res2)
        r_texts.append(response.Responses.res3)

    decs = []
    for r in r_texts:
        res = ta.tone(r).get_result()
        enc = json.dumps(res)
        dec = json.loads(enc)
        decs.append(dec)

    count = 1
    tones = []
    scores = []
    tones_dict = {}

    for dec in decs:
        for i in dec['document_tone']['tones']:
            tones.append(i['tone_name'])
            scores.append(i['score'])
            count +=1

    for value, line in zip(scores, tones):
        if line in tones_dict:
            tones_dict[line].append(value) # append the element
        else:
            tones_dict[line] = [value]

    return tones_dict

def getToneAnalysisResults(survey_id):
    ta_data = getToneAnalysis(survey_id)
    for k,v in ta_data.items():
        ta_data[k] = int(len(v))
    print(ta_data)

    return ta_data

if __name__ == "__main__":
    getToneAnalysis()
    getToneAnalysisResults()
