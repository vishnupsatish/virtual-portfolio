from flask import Markup
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms.fields.html5 import URLField, IntegerField
from wtforms_components import ColorField
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
    bio = TextAreaField('Update your bio', validators=[Length(min=2, max=200)])
    skills = StringField('Add some of your skills (comma-separated)', validators=[Length(min=2, max=80)])
    resume = FileField('Add/update a resume', validators=[FileAllowed(['pdf'])])
    submit = InlineButtonWidget('Submit Changes')

class ColorForm(FlaskForm):
    color = ColorField("Choose your theme color.", validators=[DataRequired()])
    text_color = ColorField("Choose your text color.", validators=[DataRequired()])
    submit = InlineButtonWidget('Save colors')



# image_choices = [('Image0.jpg', 'Scenic Lake with Mountains'), 
#                 ('Image1.jpg', 'Hummingbird'), 
#                 ('Image2.jpg', 'Leaves'),
#                 ('Image3.jpg' , 'Bridge and Forest'),
#                 ('Image4.jpg' , 'Beach Drink'),
#                 ('Image5.jpg' , 'Sunset Beach'),
#                 ('Image6.jpg' , 'Tea and Book'), 
#                 ('Image7.jpg' , 'Suit and Tie'),
#                 ('Image8.jpg' , 'Yoga Sunset'),
#                 ('Image9.jpg' , 'Graduation')]


# class PictureForm(FlaskForm):
#     picture1 = SelectField('Select a picture', choices=image_choices, validators=[DataRequired()]) # label can be changed
#     picture2 = SelectField('Select a picture', choices=image_choices, validators=[DataRequired()]) # label can be changed
#     picture3 = SelectField('Select a picture', choices=image_choices, validators=[DataRequired()]) # label can be changed
#     submit = InlineButtonWidget('Save Pictures')