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

def getKeywords(option):

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
                keywords=KeywordsOptions(emotion=True, sentiment=False,
                                         limit=50))).get_result()

        enc = json.dumps(response, indent=2)
        dec = json.loads(enc)
        decs.append(dec)

    kws = []
    rels = []
    key_dict = {}

    for dec in decs:
        print(dec)
        for keyword in dec['keywords']:
                if option == "frequency" and keyword['relevance'] > 0.5:
                    kws.append(keyword['text'])
                    rels.append(keyword['relevance'])
                if option == "emotion" and keyword['relevance'] > 0.5 and (keyword['text'] not in kws):
                    kws.append(keyword['text'])
                    rels.append(max(keyword['emotion']))

    for value, line in zip(rels, kws):
        if line in key_dict:
            key_dict[line].append(value) # append the element
        else:
            key_dict[line] = [value]

    return key_dict



def getKeywordAnalysisResults():
    k_data = getKeywords("frequency")
    for k,v in k_data.items():
        k_data[k] = float(sum(v)/len(v))
    return k_data


def getFrequentKeywords():
    k_data = getKeywords("frequency")
    for k,v in k_data.items():
        k_data[k] = int(len(v))
    return k_data

def getOverallKA():
    relevance = getKeywordAnalysisResults()
    freq = getFrequentKeywords()
    l = []
    ds = [relevance, freq]
    d = {}
    for k in relevance.keys():
        d[k] = list(d[k] for d in ds)

    res = []
    for key, val in d.items():
        res.append([key] + val)
    res_j = json.dumps(res)
    return res_j



if __name__ == "__main__":
    getAverageRelevance()
    getKeywords()
    getKeywordAnalysisResults()
    getFrequentKeywords()
    getOverallKA()
    getKeywordEmotion()

