import json
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('yFuCchPFCVlie95N3m1FVetEvkCNlsj1Urt8hUVNTI0P')
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)

language_translator.set_service_url('https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/d2b84c14-b9bb-4989-ae81-7fb1364906ba')


def lang(text):
        language = language_translator.identify(text).get_result()
        lcode = language['languages'][0]['language']
        print(lcode)
        return lcode
    
var = lang("I'm fine")

print(var)
