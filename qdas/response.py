import os
import glob
from flask import request


def audioResponseDir():
    i=1
    keepGoing=True
    while keepGoing:
      path = "qdas/static/audioResponses/audio_{}/".format(i)
      if not os.path.exists(path):
        path = os.makedirs(os.path.dirname("qdas/static/audioResponses/audio_{}/".format(i)), exist_ok=False)
        keepGoing = False
      i += 1

def saveResponse():
    TARGET_DIR = str(max(glob.glob(os.path.join('qdas/static/audioResponses', '*/')), key=os.path.getmtime))[:-1] + "/"
    print(TARGET_DIR)
    f = request.files['audio_data']
    i = 0
    while os.path.exists(TARGET_DIR + "audio%s.wav" % i):
        i +=1
    with open(TARGET_DIR + 'audio%s.wav' % i, 'wb') as audio:
        f.save(audio)
        print('file uploaded successfully')

if __name__ == "__main__":
    audioResponseDir()
    saveResponse()
