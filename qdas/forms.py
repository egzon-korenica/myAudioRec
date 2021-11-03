from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class QuestionForm(FlaskForm):
    question = StringField(validators=[DataRequired()], description="Write a question")


class SurveyForm(FlaskForm):
    topic = StringField('Survey Title', validators=[DataRequired()], description="Survey Title")
    questions = FieldList(FormField(QuestionForm), min_entries=1)
    add_q = SubmitField(label='Add Question')
    submit = SubmitField(label='Generate Survey')
