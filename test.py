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


surveys = db.session.query(Survey, Questions).filter(Questions.lan_code=="en").filter(Survey.id ==  Questions.survey_id).order_by(Survey.id.desc()).all()

surveys2 = Survey.query\
    .join(Questions, Survey.id==Questions.survey_id)\
    .add_columns(Survey.id, Questions.topic, Questions.q1, Questions.q2, Questions.q3)\
    .filter(Survey.id==Questions.survey_id)\
    .filter(Questions.lan_code=="en")\
    .order_by(Survey.id.desc())\
    .paginate(page=1, per_page = 4)


for survey in surveys2.items:

	print(survey.Survey.id)
