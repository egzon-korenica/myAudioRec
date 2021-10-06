from datetime import datetime
from qdas import db

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    question_ts = db.relationship('Questions', lazy=True)

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lan_code = db.Column(db.String(3), nullable=False)
    q1 = db.Column(db.String(100), nullable=False)
    q2 = db.Column(db.String(100), nullable=False)
    q3 = db.Column(db.String(100), nullable=False)
    #question_ts = db.relationship('QuestionsTranslated') backref='question_lang', lazy=True)

    def __repr__(self):
        return f"Questions('{self.q1}', '{self.q2}', '{self.q3}')"


class QuestionsTranslated(db.Model):
    __tablename__ = 'QuestionsTranslated'
    id = db.Column(db.Integer, primary_key=True)
    q_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    lan_code = db.Column(db.String(3), nullable=False)
    q1 = db.Column(db.String(100), nullable=False)
    q2 = db.Column(db.String(100), nullable=False)
    q3 = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"QuestionsTranslated('{self.lan_code}','{self.q1}', '{self.q2}', '{self.q3}')"
