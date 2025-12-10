from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=80)
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6)
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match')
    ])
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class PlantForm(FlaskForm):
    name = StringField('Plant Name', validators=[
        DataRequired(), 
        Length(min=1, max=100)
    ])
    type = SelectField('Plant Type', choices=[
        ('sunflower', '🌻 Sunflower'),
        ('rose', '🌹 Rose'),
        ('cactus', '🌵 Cactus'),
        ('tulip', '🌷 Tulip'),
        ('cherry_blossom', '🌸 Cherry Blossom'),
        ('hibiscus', '🌺 Hibiscus'),
        ('lotus', '🪷 Lotus'),
        ('seedling', '🌱 Seedling')
    ], validators=[DataRequired()])


class MoodLogForm(FlaskForm):
    note_text = TextAreaField('How are you feeling today?', validators=[
        DataRequired(), 
        Length(min=10, max=1000)
    ])


class ReminderForm(FlaskForm):
    description = StringField('Reminder', validators=[
        DataRequired(), 
        Length(min=5, max=200)
    ])
    reminder_date = DateTimeField('Date & Time', 
                                   format='%Y-%m-%dT%H:%M',
                                   validators=[DataRequired()])