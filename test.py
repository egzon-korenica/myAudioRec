from qdas import db
from qdas.models import Questions, Survey, Responses
from sqlalchemy.orm import sessionmaker
import sqlite3
import glob
import os



responses = db.session.query(Survey, Responses).join(Responses).filter(Survey.id == 1).all()

print(os.sep.join(os.path.normpath('qdas/static/audioResponses/survey_001').split(os.sep)[-1:]))

responses = db.session.query(Survey.survey_folder).filter(Survey.id == 1)
