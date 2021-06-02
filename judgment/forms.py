from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, DateTimeField
from wtforms.validators import DataRequired


class AddJudgments(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    date_of_judgment = StringField("Date of judgment", validators=[DataRequired()])
    submit = SubmitField("Add judgment")
