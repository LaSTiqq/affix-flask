from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.recaptcha import RecaptchaField


class ContactForm(FlaskForm):
    name = StringField(
        label='Vārds',
        render_kw={
            'class': 'form-control bg-transparent ms-auto mt-2',
            'placeholder': 'Vārds',
            'autocomplete': 'off',
        },
        validators=[
            DataRequired(),
            Length(min=4, max=15)
        ],
    )
    email = EmailField(
        label='E-pasts',
        render_kw={
            'class': 'form-control bg-transparent ms-auto mt-2',
            'placeholder': 'E-pasts',
            'autocomplete': 'off',
        },
        validators=[
            DataRequired(),
            Email()
        ],
    )
    subject = StringField(
        label='Temats',
        render_kw={
            'class': 'form-control bg-transparent ms-auto mt-2',
            'placeholder': 'Temats',
            'autocomplete': 'off',
        },
        validators=[
            DataRequired(),
            Length(min=5, max=25)
        ],
    )
    message = TextAreaField(
        label='Teksts',
        render_kw={
            'class': 'form-control bg-transparent me-auto ms-md-2 mt-2 pt-3',
            'placeholder': 'Teksts',
            'autocomplete': 'off',
            'rows': 5,
        },
        validators=[
            DataRequired(),
            Length(min=50)
        ],
    )
    recaptcha = RecaptchaField(label='Captcha')
