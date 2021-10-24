import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions, EntitiesOptions
from qdas import db
from qdas.models import Survey, Responses

apikey = "XJX6gQPMRUfkx0USfzHIHrrPHnH5PEPycxZkIE6xAazh"

url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/1ba469e8-195f-429f-a646-588c2d5dc3ef"

authenticator = IAMAuthenticator(apikey)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2021-03-25',
    authenticator=authenticator
)

natural_language_understanding.set_service_url(url)

def getKeywords():

    responses = db.session.query(Survey, Responses).join(Responses).filter(Survey.id == 1).all()
    r_texts = []
    for index, response in enumerate(responses):
        r_texts.append(response.Responses.res1)
        r_texts.append(response.Responses.res2)
        r_texts.append(response.Responses.res3)

    decs = []
    for r in r_texts:
        response = natural_language_understanding.analyze(
            text = r,
            features=Features(
                keywords=KeywordsOptions(emotion=False, sentiment=False,
                                         limit=50))).get_result()

        enc = json.dumps(response, indent=2)
        dec = json.loads(enc)
        decs.append(dec)

    kws = []
    rels = []
    key_dict = {}

    for dec in decs:
        for keyword in dec['keywords']:
                if keyword['relevance'] > 0.5:
                    kws.append(keyword['text'])
                    rels.append(keyword['relevance'])


    for value, line in zip(rels, kws):
        if line in key_dict:
            key_dict[line].append(value) # append the element
        else:
            key_dict[line] = [value]

    return key_dict


def getKeywordAnalysisResults():
    k_data = getKeywords()
    for k,v in k_data.items():
        k_data[k] = float(sum(v)/len(v))

    return k_data

def getFrequentKeywords():
    k_data = getKeywords()
    for k,v in k_data.items():
        k_data[k] = int(len(v))
    print(k_data)
    return k_data

if __name__ == "__main__":
    getKeywordAnalysisResults()
    getFrequentKeywords()
