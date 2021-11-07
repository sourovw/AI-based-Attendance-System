from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from blog.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Registration No.', validators=[DataRequired(), Length(min=4, max=10)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=5, max=60)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    varsity = StringField('University', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already registered.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Registration No.', validators=[DataRequired(), Length(min=4, max=10)])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=5, max=60)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    varsity = StringField('University', validators=[DataRequired(), Length(min=2, max=100)])
    pic1 = FileField('Picture 1', validators=[FileAllowed(['jpg', 'png'])])
    pic2 = FileField('Picture 2', validators=[FileAllowed(['jpg', 'png'])])
    pic3 = FileField('Picture 3', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already registered.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already registered.')
