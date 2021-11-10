import glob
import os
from pathlib import Path
from qdas import db
from qdas.models import Survey
import sqlite3

decs = {'usage': {'text_units': 1, 'text_characters': 265, 'features': 1}, 'relations': [{'type': 'employedBy', 'sentence': 'I am pleased to be here today at the World Health Organization, together with the German Health Minister to report on what we are planning the Ebola catastrophe Africa Has still painfully shown us how urgent the international need for action in crisis situations is', 'score': 0.941677, 'arguments': [{'text': 'Health Minister', 'location': [89, 104], 'entities': [{'type': 'Person', 'text': 'Health Minister'}]}, {'text': 'German', 'location': [82, 88], 'entities': [{'type': 'GeopoliticalEntity', 'text': 'German', 'disambiguation': {'subtype': ['Country']}}]}]}, {'type': 'agentOf', 'sentence': 'I am pleased to be here today at the World Health Organization, together with the German Health Minister to report on what we are planning the Ebola catastrophe Africa Has still painfully shown us how urgent the international need for action in crisis situations is', 'score': 0.60716, 'arguments': [{'text': 'Health Minister', 'location': [89, 104], 'entities': [{'type': 'Person', 'text': 'Health Minister'}]}, {'text': 'report', 'location': [108, 114], 'entities': [{'type': 'EventCommunication', 'text': 'report'}]}]}, {'type': 'affectedBy', 'sentence': 'I am pleased to be here today at the World Health Organization, together with the German Health Minister to report on what we are planning the Ebola catastrophe Africa Has still painfully shown us how urgent the international need for action in crisis situations is', 'score': 0.520645, 'arguments': [{'text': 'we', 'location': [123, 125], 'entities': [{'type': 'Person', 'text': 'we'}]}, {'text': 'report', 'location': [108, 114], 'entities': [{'type': 'EventCommunication', 'text': 'report'}]}]}], 'language': 'en'}
{'usage': {'text_units': 1, 'text_characters': 223, 'features': 1}, 'relations': [{'type': 'ownerOf', 'sentence': 'Legitimation in global health issues enjoys and therefore it is about making their structures efficient.', 'score': 0.503822, 'arguments': [{'text': 'their', 'location': [77, 82], 'entities': [{'type': 'Person', 'text': 'their'}]}, {'text': 'structures', 'location': [83, 93], 'entities': [{'type': 'Facility', 'text': 'structures'}]}]}, {'type': 'partOf', 'sentence': 'It is certainly an advantage of the World Health Organization that it has a hundred fifty country offices six regional', 'score': 0.504954, 'arguments': [{'text': 'offices', 'location': [203, 210], 'entities': [{'type': 'Organization', 'text': 'offices', 'disambiguation': {'subtype': ['Government']}}]}, {'text': 'country', 'location': [195, 202], 'entities': [{'type': 'GeopoliticalEntity', 'text': 'country', 'disambiguation': {'subtype': ['Country']}}]}]}], 'language': 'en'}
{'usage': {'text_units': 1, 'text_characters': 191, 'features': 1}, 'relations': [], 'language': 'en'}
{'usage': {'text_units': 1, 'text_characters': 191, 'features': 1}, 'relations': [], 'language': 'en'}
{'employedBy': ['I am pleased to be here today at the World Health Organization, together with the German Health Minister to report on what we are planning the Ebola catastrophe Africa Has still painfully shown us how urgent the international need for action in crisis situations is'], 'agentOf': ['I am pleased to be here today at the World Health Organization, together with the German Health Minister to report on what we are planning the Ebola catastrophe Africa Has still painfully shown us how urgent the international need for action in crisis situations is'], 'affectedBy': ['I am pleased to be here today at the World Health Organization, together with the German Health Minister to report on what we are planning the Ebola catastrophe Africa Has still painfully shown us how urgent the international need for action in crisis situations is'], 'ownerOf': ['Legitimation in global health issues enjoys and therefore it is about making their structures efficient.'], 'partOf': ['It is certainly an advantage of the World Health Organization that it has a hundred fifty country offices six regional']}

kws = []
rels = []
txt = []
key_dict = {}

for dec in decs:
            print(dec)
            for relation in dec['relations']:
                if len(relation) != 0 and relation['score'] > 0.5:
                    for arg in relation['arguments']:
                        for a in arg['text']:
                            txt.append(a)

print(txt)
