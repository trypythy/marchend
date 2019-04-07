from flask import render_template, url_for, flash, redirect, request
from flaskweb.forms import RegistrationForm, LoginForm
from flaskweb.models import User, Review
from flaskweb import app, db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required


reviews = [
	{
		'author': 'bt',
		'title': 'black mirror',
		'content': 'Futuristic, Dark, Inevitable',
		'date_posted': 'March 29, 2019'
	},
	{
		'author': 'jt',
		'title': 'star trek discovery',
		'content': 'Fantasy, Space, Worm holes',
		'date_posted': 'March 29, 2019'
	}

]

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', reviews=reviews)

@app.route('/about')
def about():
	return render_template('about.html', title='About Us')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created - welcome, please login', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			flash('Logged in successfully', 'success')
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
	logout_user()
	flash('Logged out successfully', 'success')
	return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
	return render_template('account.html', title='My Account')





