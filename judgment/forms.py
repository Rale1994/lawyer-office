from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired


class AddJudgments(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    date = DateTimeLocalField("Date of judgment", format='%Y-%m-%d')
    submit = SubmitField("Add judgment")
