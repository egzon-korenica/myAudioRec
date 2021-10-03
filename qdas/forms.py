from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class SurveyForm(FlaskForm):
    q1 = StringField('Question 1', validators=[DataRequired()], description="Write a question")
    q2 = StringField('Question 2', validators=[DataRequired()], description="Write a question")
    q3 = StringField('Question 3', validators=[DataRequired()], description="Write a question")
