import json
import operator
from ibm_watson import NaturalLanguageUnderstandingV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions, EntitiesOptions, RelationsOptions, ConceptsOptions
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
        if len(r) > 0 and option != "relation" and option != "entity" and option != "concepts":
            try:
                response = natural_language_understanding.analyze(
                    text=r,
                    features=Features(
                        keywords=KeywordsOptions(emotion=True, sentiment=False,
                                                 limit=50))).get_result()

                enc = json.dumps(response, indent=2)
                dec = json.loads(enc)
                decs.append(dec)
            except ApiException as ex:
                print("Method failed with status code " + str(ex.code) + ": " + ex.message)

        if len(r) > 0 and option == "relation" or option == "entity":
            try:
                response = natural_language_understanding.analyze(
                    text=r,
                        features=Features(relations=RelationsOptions())).get_result()

                enc = json.dumps(response, indent=2)
                dec = json.loads(enc)
                decs.append(dec)
            except ApiException as ex:
                print("Method failed with status code " + str(ex.code) + ": " + ex.message)

        if len(r) > 0 and option == "concepts":
            try:
                response = natural_language_understanding.analyze(
                    text=r,
                    features=Features(concepts=ConceptsOptions(limit=3))).get_result()

                enc = json.dumps(response, indent=2)
                dec = json.loads(enc)
                decs.append(dec)
            except ApiException as ex:
                print("Method failed with status code " + str(ex.code) + ": " + ex.message)

    kws = []
    rels = []
    key_dict = {}

    for dec in decs:
        if option != "relation" and option != "entity" and option != "concepts":
            for keyword in dec['keywords']:
                if option == "frequency" and keyword['relevance'] > 0.5:
                    kws.append(keyword['text'])
                    rels.append(keyword['relevance'])
                if option == "emotion" and keyword['relevance'] > 0.5 and (keyword['text'] not in kws):
                    kws.append(keyword['text'])
                    rels.append(max(keyword['emotion'].items(), key=operator.itemgetter(1))[0])

        if option == "relation":
            for relation in dec['relations']:
                args = []
                if len(relation) != 0 and relation['score'] > 0.5:
                    kws.append(relation['type'])
                    args.append(relation['sentence'])
                    for arg in relation['arguments']:
                        args.append(arg['text'])
                    rels.append(args)


        if option == "entity":
            for relation in dec['relations']:
                if len(relation) != 0 and relation['score'] > 0.5:
                    for arg in relation['arguments']:
                        for entity in arg['entities']:
                            kws.append(entity['type'])
                            rels.append(entity['text'])

        if option == "concepts":
            for concept in dec['concepts']:
                if len(concept) != 0 and concept['relevance'] > 0.5:
                    rels.append(concept['text'])
                    kws.append(concept['relevance'])

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
    return new_dict

def getRelations(survey_id):
    relations_dict = getKeywords("relation", survey_id)
    return relations_dict

def getEntities(survey_id):
    entities_dict = getKeywords("entity", survey_id)
    return entities_dict

def getConcepts(survey_id):
    concepts_dict = getKeywords("concepts", survey_id)
    c_list = []
    for key, value in concepts_dict.items():
        temp_list = []
        temp_list.append(round(key, 3))
        temp_list.append(value)
        c_list.append(temp_list)
    print(c_list)
    return c_list

if __name__ == "__main__":
    getKeywords()
    getKeywordAnalysisResults()
    getFrequentKeywords()
    getOverallKA()
    getKeywordEmotion()
