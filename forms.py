from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, 
						IntegerField, DateField, PasswordField)
from wtforms.validators import (DataRequired, Optional, Regexp, 
								ValidationError, Email, Length, EqualTo)

from models import Journal, User



def name_exists(form, field):
	if User.select().where(User.username == field.data).exists():
		raise ValidationError('User with that name already exists.')


def email_exists(form, field):
	if User.select().where(User.email == field.data).exists():
		raise ValidationError('User with that email already exists.')


class RegisterForm(FlaskForm):
	username = StringField(
		'username',
		validators=[
			DataRequired(),
			Regexp(
				r'^[a-zA-Z0-9_]+$',
				message=("Username should be one word, letters, "
						"numbers, and underscores only.")
			),
			name_exists
		])
	email = StringField(
		'Email',
		validators=[
			DataRequired(),
			Email(),
			email_exists
		])
	password = PasswordField(
		'Password',
		validators=[
			DataRequired(),
			Length(min=2),
			EqualTo('password2', message='Passwords must match')
	])
	password2 = PasswordField(
		'Confirm Password',
		validators=[DataRequired()]
	)


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])


class JournalForm(FlaskForm):
	title = StringField(
		'Title',
		validators=[DataRequired()])
	date = DateField(
		'Date',
		validators=[Optional(),])
	time_spent = IntegerField(
		'Time spent',
		validators=[DataRequired()])
	what_i_learned = TextAreaField(
		'What I learned',
		validators=[DataRequired()])
	to_remember = TextAreaField(
		'To remember',
		validators=[DataRequired()])