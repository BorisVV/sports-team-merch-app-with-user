from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired("Please enter a name.")])
    email = StringField('Email', validators=[DataRequired("Please enter a valid email.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password.")])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Please enter your email address"), Email("Please enter a valid email address")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password")])
    submit = SubmitField("Sign in")
