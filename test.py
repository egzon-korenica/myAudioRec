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

text = []
for index, response in enumerate(responses):
	text.append(response.Responses.res1)
	text.append(response.Responses.res2)
	text.append(response.Responses.res3)

	
s1 = AudioSegment.from_file(src, format="wav")
s1.export(dst, format='mp3', parameters=["-ac","2","-ar","8000"])
