from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField, DateField, TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired, Email, URL, Length
from flask_wtf.file import FileField, FileAllowed, FileRequired


class LoginForm(FlaskForm):
    userEmail = StringField('Email address', validators=[DataRequired(), Email('Enter a valid email')])
    userPassword = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    userfirstname = StringField('First Name', validators=[DataRequired()])
    userlastname = StringField('Last Name', validators=[DataRequired()])
    userregemail = StringField('Email address', validators=[DataRequired(), Email()])
    userregpwd = PasswordField('Password', validators=[DataRequired()])
    userdateofbirth = DateField('Date Of Birth', validators=[DataRequired()])
    # usergender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    agree = BooleanField('I agree to the terms and conditions', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class BlogPostForm(FlaskForm):
    post_title = StringField('Blog Title', validators=[DataRequired(), Length(max=200)])
    post_image = FileField('Add Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], "we only allow images")])
    post_content = TextAreaField('Post Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    post_description = TextAreaField('Post Description', validators=[DataRequired(), Length(max=100)] )
    status = RadioField('Status', choices=[('1', 'Publish'), ('0', 'Draft')], validators=[DataRequired()])
    categories = SelectField('Category', choices=[
        ('Academic', 'Academic'),
        ('Technical', 'Technical'),
        ('Creative', 'Creative'),
        ('Poetry', 'Poetry'),
        ('Journalistic', 'Journalistic'),
        ('Business', 'Business'),
        ('Food and Recipe', 'Food and Recipe'),
        ('Nature', 'Nature'),
        ('Humor', 'Humor'),
    ], validators=[DataRequired()])

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    bio = TextAreaField('Bio')
    facebook = StringField('Facebook @', validators=[URL('Enter a Valid URL')])
    instagram = StringField('Instagram @', validators=[URL('Enter a Valid URL')])
    x = StringField('X @', validators=[URL('Enter a Valid URL')])
    github = StringField('GitHub @', validators=[URL('Enter a Valid URL')])
    email = StringField('Email @', validators=[Email(message="Enter a Valid Gmail address")])
    # image = FileField('Upload Cover', validators=[FileAllowed(['jpg', 'jpeg', 'png'], "we only allow images")])
    submit = SubmitField('Update Profile')

class UpdateBlogPostForm(FlaskForm):
    updated_title = StringField('Title', validators=[DataRequired()])
    updated_description = TextAreaField('Description', validators=[DataRequired()])
    updated_content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Update Post')

class CommentForm(FlaskForm):
    comment_content = StringField('What Do You Think', validators=[DataRequired()])
    submit = SubmitField('Comment')

class AnnouncementForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])