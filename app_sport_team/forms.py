from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField

class SignupForm(Form):
    name = StringField('Name')
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Submit')
