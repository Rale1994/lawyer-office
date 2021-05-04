from flask_wtf import FlaskForm
from wtforms import SelectField


class AddJudgments(FlaskForm):
    client_name = SelectField('client_name', choices=[])
