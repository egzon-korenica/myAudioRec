from qdas import db
from qdas.models import Questions, Survey
from sqlalchemy.orm import sessionmaker
import sqlite3
import glob
import os



TARGET_DIR = str(max(glob.glob(os.path.join('qdas/static/audioResponses', '*/')), key=os.path.getmtime))[:-1] + "/"
#print(TARGET_DIR)

rootdir = 'qdas/static/audioResponses/'

dir = []
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        path = os.path.join(subdir, file)
        dir.append(path)
        
print(dir, len(dir))

print(os.path.basename(os.path.normpath('qdas/static/audioResponses/survey_001/audio_00003')))
    

