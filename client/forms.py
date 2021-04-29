from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class AddClient(FlaskForm):
    f_name = StringField("First name", validators=[DataRequired()])
    l_name = StringField("Last name", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    phone = StringField("Phone number", validators=[DataRequired()])
    mail = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Add client")
