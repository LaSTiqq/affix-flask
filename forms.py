from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.recaptcha import RecaptchaField


class ContactForm(FlaskForm):
    name = StringField(
        label='Vārds',
        id='name',
        render_kw={
            'class': 'form-control mb-2',
            'placeholder': 'Vārds',
            'autocomplete': 'off',
        },
        validators=[
            DataRequired(),
            Length(min=3, max=15)
        ],
    )
    email = EmailField(
        label='E-pasts',
        id='email',
        render_kw={
            'class': 'form-control my-2',
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
        id='subject',
        render_kw={
            'class': 'form-control my-2',
            'placeholder': 'Temats',
            'autocomplete': 'off',
        },
        validators=[
            DataRequired(),
            Length(min=5, max=25)
        ],
    )
    message = TextAreaField(
        label='Ziņojums',
        id='message',
        render_kw={
            'class': 'form-control my-2',
            'placeholder': 'Ziņojums',
            'autocomplete': 'off',
        },
        validators=[
            DataRequired(),
            Length(min=20)
        ],
    )
    recaptcha = RecaptchaField(label='Captcha')
