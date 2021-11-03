import json
import operator
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


def getKeywords(option, survey_id):
    responses = db.session.query(Survey, Responses).join(Responses).filter(Survey.id == survey_id).filter(
        Responses.lan_code == "en").all()
    r_texts = []
    for index, response in enumerate(responses):
        for res in response.Responses.responses:
            r_texts.append(res)

    decs = []
    for r in r_texts:
        if len(r) > 0:
            response = natural_language_understanding.analyze(
                text=r,
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
        for keyword in dec['keywords']:
            if option == "frequency" and keyword['relevance'] > 0.5:
                kws.append(keyword['text'])
                rels.append(keyword['relevance'])
            if option == "emotion" and keyword['relevance'] > 0.5 and (keyword['text'] not in kws):
                kws.append(keyword['text'])
                rels.append(max(keyword['emotion'].items(), key=operator.itemgetter(1))[0])

    for value, line in zip(rels, kws):
        if line in key_dict:
            key_dict[line].append(value)  # append the element
        else:
            key_dict[line] = [value]

    return key_dict


def getKeywordAnalysisResults(survey_id):
    k_data = getKeywords("frequency", survey_id)
    for k, v in k_data.items():
        k_data[k] = float(sum(v) / len(v))
    return k_data


def getFrequentKeywords(survey_id):
    k_data = getKeywords("frequency", survey_id)
    for k, v in k_data.items():
        k_data[k] = int(len(v))
    return k_data


def getOverallKA(survey_id):
    relevance = getKeywordAnalysisResults(survey_id)
    freq = getFrequentKeywords(survey_id)
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


def getKeywordEmotion(survey_id):
    emotions_dict = getKeywords("emotion", survey_id)
    new_dict = {i: str(j[0]) for i, j in emotions_dict.items()}
    print(new_dict)
    return new_dict


def getAverageRelevance(listoflist):
    relevances = []
    data = json.loads(listoflist)
    for l in data:
        relevances.append(l[1])
    avg = sum(relevances) / len(relevances)
    avgf = '{:.5f}'.format(avg)

    return avgf


if __name__ == "__main__":
    getAverageRelevance()
    getKeywords()
    getKeywordAnalysisResults()
    getFrequentKeywords()
    getOverallKA()
    getKeywordEmotion()
