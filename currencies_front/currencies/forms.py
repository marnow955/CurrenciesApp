from flask_wtf import FlaskForm
from wtforms import SubmitField, DateField
from wtforms.validators import DataRequired


class CurrencyForm(FlaskForm):
    start_date = DateField('Od', validators=[DataRequired()], render_kw={"placeholder": "Data od"})
    end_date = DateField('Do', validators=[DataRequired()], render_kw={"placeholder": "Data do"})
    submit = SubmitField('Filtruj')
