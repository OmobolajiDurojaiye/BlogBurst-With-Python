from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField, DateField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, URL


class LoginForm(FlaskForm):
    userEmail = StringField('Email address', validators=[DataRequired(), Email()])
    userPassword = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    userfirstname = StringField('First Name', validators=[DataRequired()])
    userlastname = StringField('Last Name', validators=[DataRequired()])
    userregemail = StringField('Email address', validators=[DataRequired(), Email()])
    userregpwd = PasswordField('Password', validators=[DataRequired()])
    userdateofbirth = DateField('Date Of Birth', validators=[DataRequired()])
    usergender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    agree = BooleanField('I agree to the terms and conditions', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class BlogPostForm(FlaskForm):
    post_title = StringField('Blog Title', validators=[DataRequired()])
    post_image = FileField('Add Image')
    post_content = TextAreaField('Post Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    facebook = StringField('Facebook @', validators=[URL()])
    instagram = StringField('Instagram @', validators=[URL()])
    x = StringField('X @', validators=[URL()])
    email = StringField('E-Mail @', validators=[Email()])
    github = StringField('GitHub @', validators=[URL()])