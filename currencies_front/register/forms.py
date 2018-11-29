from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    first_name = StringField('Imie', validators=[DataRequired()])
    last_name = StringField('Nazwisko', validators=[DataRequired()])
    username = StringField('Nick', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Haslo', validators=[DataRequired()])
    password2 = PasswordField(
        'Powtorz haslo', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Rejestruj')
