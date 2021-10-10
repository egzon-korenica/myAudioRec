from qdas import db
from qdas.models import Questions, Survey
from sqlalchemy.orm import sessionmaker


result = db.session.query(Survey, Questions).filter(Questions.lan_code=="en").filter(Survey.id == Questions.survey_id).all()

#for row in result:
 # print("survey_id", row.Survey.id, "Q1:", row.Questions.q1, "Q1:", row.Questions.q1, "Q2:", row.Questions.q2, "Q3:", row.Questions.q3)
  
query = db.session.query(Questions).filter(Questions.lan_code=="en").first()

voices = {
  "ar": "ar-AR_OmarVoice",
  "de": "de-DE_BirgitV3Voice",
  "en": "en-GB_KateV3Voice",
  "es": "es-ES_EnriqueV3Voice",
  "fr": "fr-CA_LouiseV3Voice"
  #"it": "Mustang",
  #"ja": "Mustang",
  #"ko": "Mustang",
  #"nl": "Mustang",
  #"pt": "Mustang",
  #"de": "Mustang",
  #"zh": "Mustang"
}

currentSurvey = db.session.query(Survey).order_by(Survey.id.desc()).first()
survey= db.session.query(Questions).filter(Questions.survey_id == currentSurvey.id, Questions.lan_code == "en").all()
#surveys = db.session.query(Survey, Questions).filter(Survey.id == survey_id).filter(Survey.id == Questions.survey_id).all()

#for row in survey:
 #   print("survey_id", row.Survey.id, "Q1:", row.Questions.q1, "Q2:", row.Questions.q2, "Q3:", row.Questions.q3)


#for key in voices:
 #   print(key)

def read2(lcode):
    currentSurvey = db.session.query(Survey).order_by(Survey.id.desc()).first()
    surveyQuestions= db.session.query(Questions).filter(Questions.survey_id == currentSurvey.id, Questions.lan_code == lcode).all()
    text = []
    #print(surveyQuestions)
    for question in surveyQuestions:
        print(question[:2])
        text.append(question.q1)
        text.append(question.q2)
        text.append(question.q3)
    return text    


#surveys = db.session.query(Survey, Questions).filter(Questions.lan_code=="en").filter(Survey.id == Questions.survey_id).all()
surveys = db.session.query(Survey, Questions).join(Survey).filter(Survey.id == 1).filter(Questions.lan_code=="en").all()
for survey in surveys:
    print(survey.Survey.id)


