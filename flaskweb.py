# flaskweb.py
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'edc163356e4062185ed45a71c376d95c'

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
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f'Yay! Account created successfully for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'bt@bt.com' and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful. Please check username and password', 'danger')
	return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
	app.run(debug=True)