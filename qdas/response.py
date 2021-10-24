import os
import glob
from flask import request
from pydub import AudioSegment


def audioResponseDir(folderType):
    i= 1
    keepGoing=True
    if folderType == "audio":
        TARGET_DIR = str(max(glob.glob(os.path.join('qdas/static/audioResponses', '*/')), key=os.path.getmtime))[:-1] + "/"
        while keepGoing:
          path = TARGET_DIR + "/audio_{:05d}/".format(i)
          if not os.path.exists(path):
            path = os.makedirs(os.path.dirname(TARGET_DIR + "/audio_{:05d}/".format(i)), exist_ok=False)
            keepGoing = False
          i += 1
    if folderType == "survey":
        while keepGoing:
          path = "qdas/static/audioResponses/survey_{:03d}/".format(i)
          if not os.path.exists(path):
            path = os.makedirs(os.path.dirname("qdas/static/audioResponses/survey_{:03d}/".format(i)), exist_ok=False)
            keepGoing = False
          i += 1
    else:
        print("no directory name provided")

def saveResponse():
    SURVEY_DIR = str(max(glob.glob(os.path.join('qdas/static/audioResponses', '*/')), key=os.path.getmtime))[:-1] + "/"
    TARGET_DIR = str(max(glob.glob(os.path.join(SURVEY_DIR, '*/')), key=os.path.getmtime))[:-1] + "/"
    f = request.files['audio_data']
    i = 0
    while os.path.exists(TARGET_DIR + "/audio{:02d}.wav".format(i)):
        i +=1
    with open(TARGET_DIR + '/audio{:02d}.wav'.format(i), 'wb') as audio:
        f.save(audio)
        print('file uploaded successfully')

if __name__ == "__main__":
    audioResponseDir()
    saveResponse()
