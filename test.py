import glob
import os
from pathlib import Path
from qdas import db
from qdas.models import Survey
import sqlite3

SURVEY_DIR = str(max(glob.glob(os.path.join('qdas/static/audioResponses', '*/')), key=os.path.getmtime))[:-1] + "/"


def deleteRes(pfolder):
    p = str(pfolder)
    print(p)
    conn = sqlite3.connect('qdas/site.db')
    print("Opened database successfully")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Responses where participant_folder = ?", (p,))
    conn.commit()
    print("Row deleted successfully")
    

deleteRes('survey_001/audio_00001')
