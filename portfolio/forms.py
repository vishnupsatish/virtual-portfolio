from flask import Markup
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms.fields.html5 import URLField, IntegerField
from portfolio.models import User
import datetime


class InlineButtonWidget(object):
    html = """
    <button %s type="submit">%s</button>
    """

    def __init__(self, label, input_type='submit'):
        self.input_type = input_type
        self.label = label

    def __call__(self, **kwargs):
        param = []
        for key in kwargs:
            param.append(key + "=\"" + kwargs[key] + "\"")
        return Markup(self.html % (" ".join(param), self.label))


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Full Name', validators=[DataRequired(), Length(min=4, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    bio = TextAreaField('Biography', validators=[DataRequired(), Length(min=10,max=200)])
    submit = InlineButtonWidget('Sign Up')

    def validate_username(self, username):
        try:
            user = User.query.filter_by(username=username.data)[0]
        except:
            return
        raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        try:
            user = User.query.filter_by(email=email.data)[0]
        except:
            return
        raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = InlineButtonWidget('Login')



class AddJobForm(FlaskForm):
    name = StringField('Name of Company', validators=[DataRequired(), Length(min=2, max=40)])
    role = StringField('Your role (ex: Software Developer)', validators=[DataRequired(), Length(min=2, max=40)])
    description = TextAreaField('What you did, skills you acquired and anything else you want your future employers to see.', validators=[DataRequired(), Length(min=10, max=200)])
    start_date = StringField('Start Date', validators=[DataRequired()])
    end_date = StringField('End Date (Optional)')
    volunteer = BooleanField('Volunteer? (No pay)')



class AddAchievementForm(FlaskForm):
    name = StringField('What was your achievement?', validators=[DataRequired(), Length(min=2, max=40)])
    description = TextAreaField('Give a short description about the achievement and how you earned it.', validators=[DataRequired(), Length(min=10, max=200)])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(1900,datetime.datetime.now().year)])


class AddProjectForm(FlaskForm):
    name = StringField('What is the name of the project?', validators=[DataRequired(), Length(min=2, max=40)])
    description = TextAreaField('Give a short description about the project.', validators=[DataRequired(), Length(min=10, max=200)])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(1900,datetime.datetime.now().year)])
    url = URLField('URL of Project', validators=[DataRequired()])


class UpdateProfileForm(FlaskForm):
    bio = TextAreaField('Update your bio', validators=[DataRequired()])
    skills = StringField('Add some of your skills (comma-separated)', validators=[DataRequired()])
    resume = FileField('Add/update a resume', validators=[FileAllowed(['pdf'])])
    submit = InlineButtonWidget('Submit Changes')


