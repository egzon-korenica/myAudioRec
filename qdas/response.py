import os
import glob
from flask import request
from pydub import AudioSegment


rootdir = 'qdas/static/audioResponses'

def audioResponseDir(sf):
    i= 1
    keepGoing=True
    full_path = rootdir + "/" + sf
    while keepGoing:
      path = full_path + "/audio_{:05d}/".format(i)
      if not os.path.exists(path):
        path = os.makedirs(os.path.dirname(full_path + "/audio_{:05d}/".format(i)), exist_ok=False)
        keepGoing = False
      i += 1

def surveyDir():
    i= 1
    keepGoing=True
    while keepGoing:
      path = rootdir + "/survey_{:03d}/".format(i)
      if not os.path.exists(path):
        path = os.makedirs(os.path.dirname(rootdir + "/survey_{:03d}/".format(i)), exist_ok=False)
        keepGoing = False
      i += 1

def saveResponse(lg, sf):
    print(lg)
    f = request.files['audio_data']
    i = 0
    full_path = rootdir + "/" + sf
    TARGET_DIR = str(max(glob.glob(os.path.join(full_path, '*/')), key=os.path.getmtime))[:-1] + "/"
    while os.path.exists(TARGET_DIR + "/audio{:02d}".format(i) + "-" + lg + ".wav"):
        i +=1
    with open(TARGET_DIR + "/audio{:02d}".format(i) + "-" + lg + ".wav", 'wb') as audio:
        f.save(audio)
        print('file uploaded successfully')

if __name__ == "__main__":
    audioResponseDir()
    saveResponse()
    surveyDir()
