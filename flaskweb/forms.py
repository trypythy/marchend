from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskweb import db
from flaskweb.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
	"""form for registration"""
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("This username exists, please choose another one")
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("This email exists, please choose another one")

class LoginForm(FlaskForm):
	"""form for Login"""
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	"""form for update account view"""
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Update')
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if username.data != current_user.username:
			if user:
				raise ValidationError("This username exists already, please choose another one")
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if email.data != current_user.email:
			if user:
				raise ValidationError("This email exists, please choose another one")

class ReviewForm(FlaskForm):
	"""form for a new review view"""
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Review', validators=[DataRequired()])
	submit = SubmitField('Save')


