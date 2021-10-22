from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
import subprocess


APIKEY = "bHu1STJdEgOa12vLPoSeC1VzuvZvV22sigeRg93hixsF"
URL = "https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/81d71fa0-e15b-4f65-a075-f2115ab3354e"

authenticator = IAMAuthenticator(APIKEY)
stt = SpeechToTextV1(authenticator = authenticator)
stt.set_service_url(URL)

def convertToText(dir):
    files = []
    for filename in os.listdir(dir):
        if filename.endswith('.wav'):
            files.append(filename)
    files.sort()

    results = []
    for filename in files:
        with open(dir + filename,'rb') as f:
            res = stt.recognize(audio=f, content_type='audio/wav', model='en-US_NarrowbandModel', inactivity_timeout=300).get_result()
            results.append(res)

    #print(results)

    text = []
    for file in results:
        for result in file['results']:
            text.append(result['alternatives'][0]['transcript'].rstrip())

    with open(dir + 'output.txt', 'w') as out:
        out.writelines(text)

def loopDirs(rootdir):
    paths = []
    for root,dirs,files in os.walk(rootdir):
        if not dirs:
            paths.append(root)
    return paths

audioDirs = loopDirs('qdas/static/audioResponses/')
print(audioDirs)
for audioDir in audioDirs:
    convertToText(audioDir + '/')
