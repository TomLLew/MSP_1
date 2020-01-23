from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, IntegerField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, Email, EqualTo, ValidationError
from application.models import User, Post
from flask_login import LoginManager, current_user


class RegistrationForm(FlaskForm):
    first_name = StringField('Name: ',
        validators=[
            DataRequired(),
            Length(min=2, max=60)
        ]
    )

    last_name = StringField('Surname: ',
        validators=[
            DataRequired(),
            Length(min=2, max=60)
        ]
    )

    email = StringField('Email: ',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField('Password: ',
        validators=[
            DataRequired()
        ]
    )

    confirm_password = PasswordField('Confirm Password: ',
        validators=[
            DataRequired(),
            EqualTo('password')
        ]
    )

    profile_pic = FileField('Upload Picture: ',
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email is already in use, please try another')


class LoginForm(FlaskForm):
    email = StringField('Email: ',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField('Password: ',
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    post = StringField('Post: ',
        validators=[
            DataRequired(),
            Length(min=2, max=100)
        ]
    )

    submit = SubmitField('Post')