from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class AddJudgments(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    date_of_judgment = StringField("Date of judgment", validators=[DataRequired()])
    # document = FileField('Add document ', validators=[FileAllowed(['doc', 'pdf'])])
    submit = SubmitField("Add judgment")
