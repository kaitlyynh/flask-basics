
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    email_address = StringField('Email', validators=[DataRequired(), Length(min=5), Email()])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    password2 = PasswordField('Type your password again', validators=[EqualTo('password1', message='Passwords must match')])
    submit = SubmitField('Create my account', validators=[DataRequired()])

class MakePost(FlaskForm):
    body = StringField('Make a post:', validators=[DataRequired(), Length(max=250)])
    submit_post = SubmitField('Send to feed', validators=[DataRequired()])

class SignIn(FlaskForm):
    sign_user = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    sign_pass = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    sign_submit = SubmitField('Log in', validators=[DataRequired()])
