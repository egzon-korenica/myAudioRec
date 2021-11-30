import os
import shutil
import glob
from threading import Thread
from qdas import db, translation, response, querys, tts
from qdas.models import Survey, Responses, Questions
from qdas.stt import stt, models
from ibm_watson import SpeechToTextV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

PROGRESSES = dict()


class convert(Thread):
    def __init__(self, survey, root, id):
        Thread.__init__(self)
        self.progress = 0
        self.own_id = id
        self.steps = 0
        self.neededToDo = []

        paths = []
        survey_dir = db.session.query(Survey.survey_folder).filter(
            Survey.id == survey).scalar()
        for root, dirs, files in os.walk(root + "/" + survey_dir):
            if not dirs:
                paths.append(root)

        folder_names = [
            responses.participant_folder for responses in Responses.query.all()]
        for audioDir in paths:
            print(audioDir)
            if os.sep.join(os.path.normpath(audioDir).split(os.sep)[-2:]) in folder_names:
                print("these responses have been converted")
            elif len(os.listdir(audioDir)) == 0:
                print("Directory is empty")
                shutil.rmtree(audioDir)
            else:
                print("convert")
                files = [f_name for f_name in os.listdir(
                    audioDir + "/") if f_name.endswith(".wav")]
                files.sort()
                lg = files[0][-6:-4]
                self.steps += len(files)
                if lg != "en":
                    self.steps += len(files)

                self.neededToDo.append((audioDir + '/', survey, files, lg))

    def run(self):
        for (dir, survey_id, files, lg) in self.neededToDo:
            results = []
            for filename in files:
                with open(dir + filename, 'rb') as f:
                    try:
                        res = stt.recognize(audio=f, content_type='audio/wav', smart_formatting=True, model=models.get(lg),
                                            inactivity_timeout=300).get_result()
                        results.append(res)
                        self.progress += 1
                    except ApiException as ex:
                        print("Method failed with status code " +
                              str(ex.code) + ": " + ex.message)

            text = []
            for file in results:
                record = []
                for result in file['results']:
                    record.append(result['alternatives']
                                  [0]['transcript'].rstrip())
                full_sentence = (" ".join(record))
                text.append(full_sentence)
            survey = db.session.query(Survey).order_by(
                Survey.id.desc()).get(survey_id)
            # if len(text) == nr_responses:
            responses = Responses(lan_code=lg, responses=text,
                                  participant_folder=os.sep.join(os.path.normpath(dir).split(os.sep)[-2:]))
            survey.response_ts.append(responses)
            db.session.commit()

            if lg != "en":
                # translate
                t_text = translation.translateResponse(text, lg)
                self.progress += len(files)
                translation.addResponseToDatabase(t_text, dir, survey_id)
        del PROGRESSES[self.own_id]


class create(Thread):
    def __init__(self, topic, questionData, question_num, id):
        Thread.__init__(self)
        self.step = 0
        self.own_id = id
        self.questionData = questionData
        self.topic = topic
        self.question_num = question_num

    def run(self):
        self.step = 0
        survey_lang = translation.identifySurveyLang(self.questionData[0])
        self.step += 1
        questions = Questions(lan_code=survey_lang,
                              topic=self.topic, questions=self.questionData)
        self.step += 1
        response.surveyDir()
        self.step += 1
        sf = str(max(glob.glob(os.path.join(
            'qdas/static/audioResponses/', '*/')), key=os.path.getmtime))[:-1]
        self.step += 1
        survey_folder = os.sep.join(os.path.normpath(sf).split(os.sep)[-1:])
        self.step += 1
        survey = Survey(question_ts=[questions], survey_folder=survey_folder)
        self.step += 1
        db.session.add(survey)
        self.step += 1
        db.session.commit()
        self.step += 1
        text = querys.rows()
        self.step += 1
        t_text = translation.translate(text)
        self.step += 1
        translation.addToDatabase(t_text, self.question_num)
        self.step += 1
        tts.audioDir()
        self.step += 1
        TARGET_DIR = str(max(glob.glob(os.path.join(
            'qdas/static/audios', '*/')), key=os.path.getmtime))[:-1] + "/"
        self.step += 1
        currentSurvey = db.session.query(
            Survey).order_by(Survey.id.desc()).first()
        self.step += 1
        tts.createAudioFiles(TARGET_DIR, currentSurvey.id)
        self.step += 1
        del PROGRESSES[self.own_id]
