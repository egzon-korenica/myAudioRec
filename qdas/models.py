from datetime import datetime
from qdas import db

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    q1 = db.Column(db.String(100), nullable=False)
    q2 = db.Column(db.String(100), nullable=False)
    q3 = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Questions('{self.q1}', '{self.q2}', '{self.q3}')"
