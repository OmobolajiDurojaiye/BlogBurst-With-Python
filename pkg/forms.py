from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    userEmail = StringField('Email address', validators=[DataRequired(), Email()])
    userPassword = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')