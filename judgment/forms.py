from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired


class AddJudgments(FlaskForm):
    client_name = SelectField('client_name', choices=[])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    date = DateField("Date of judgment", format='%Y-%m-%d')
    submit = SubmitField("Add judgment")
