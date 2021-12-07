import json
import os
import subprocess
import shutil
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from qdas import db, translation
from qdas.models import Survey, Responses



APIKEY = "1njZRQgYAuB2NBFFj2azPrFYdP2mLcaQtcBdkSPUaFlC"
URL = "https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/9c3ec9fa-b798-44f6-9f3d-67f8406f20a0/"

authenticator = IAMAuthenticator(APIKEY)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(URL)

# 

with open('qdas/static/audioResponses/survey_006/audio_00002/audio00-cs.wav', 'rb') as f:
            try:
                res = stt.recognize(audio=f, content_type='audio/wav', smart_formatting=False, model="cz-CZ_Telephony",
                                    inactivity_timeout=300).get_result()
                results.append(res)
            except ApiException as ex:
                print("Method failed with status code " + str(ex.code) + ": " + ex.message)


