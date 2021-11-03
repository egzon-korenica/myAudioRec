import json
from datetime import datetime
from qdas import db


class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    survey_folder = db.Column(db.String(100), nullable=False)
    question_ts = db.relationship('Questions', cascade='all,delete', lazy=True)
    response_ts = db.relationship('Responses', cascade='all,delete', lazy=True)

    def __repr__(self):
        return f"Survey('{self.id}','{self.date_posted}', '{self.survey_folder}')"


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lan_code = db.Column(db.String(3), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    questions = db.Column(db.JSON(), nullable=False)

    def __repr__(self):
        return f"Questions('{self.lan_code}','{self.topic}','[" + ", ".join(self.questions) + "]')"


class Responses(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lan_code = db.Column(db.String(3), nullable=True)
    responses = db.Column(db.JSON(), nullable=False)
    participant_folder = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Responses('{self.lan_code}','{self.participant_folder}','[" + ", ".join(self.responses) + "]')"
