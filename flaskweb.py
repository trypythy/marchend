# flaskweb.py
from flask import Flask, render_template
app = Flask(__name__)

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
def hello():
	return render_template('home.html', reviews=reviews)

@app.route('/about')
def about():
	return render_template('about.html', title='About Us')


if __name__ == '__main__':
	app.run(debug=True)