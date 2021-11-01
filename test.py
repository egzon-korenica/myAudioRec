from qdas import db
from qdas.models import Questions, Survey, Responses
from sqlalchemy.orm import sessionmaker
import sqlite3
import glob
import os
from pydub import AudioSegment


responses = db.session.query(Survey, Responses).join(Responses).filter(Survey.id == 1).all()

#print(os.sep.join(os.path.normpath('qdas/static/audioResponses/survey_001').split(os.sep)[-1:]))

#responses = db.session.query(Survey.survey_folder).filter(Survey.id == 1).all()

src = "qdas/static/audioResponses/survey_001/audio_00002/audio01.wav"
dst = "qdas/static/audioResponses/survey_001/audio_00002/audio01.mp3"


#print(len(next(os.walk('qdas/static/audioResponses/survey_001'))[1]))


listoflist = [["meeting today", 0.983223, 2], ["HESITATION fail", 0.842578, 2], ["October", 0.788983, 2], ["HESITATION ache", 0.95254, 2], ["birthday", 0.919812, 2]]

relevances = []
for l in listoflist:
	relevances.append(l[1])
	
avg = sum(relevances)/len(relevances)

avgf = '{:.5f}'.format(avg)

print(avgf)
	
