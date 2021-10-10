from datetime import datetime
from qdas import db

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    question_ts = db.relationship('Questions', lazy=True)

    def __repr__(self):
        return f"Survey('{self.id}')"


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lan_code = db.Column(db.String(3), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    q1 = db.Column(db.String(100), nullable=False)
    q2 = db.Column(db.String(100), nullable=False)
    q3 = db.Column(db.String(100), nullable=False)
    #question_ts = db.relationship('QuestionsTranslated') backref='question_lang', lazy=True)

    def __repr__(self):
        return f"Questions('{self.lan_code}','{self.topic}', '{self.q1}', '{self.q2}', '{self.q3}')"
