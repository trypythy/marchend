import os, secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskweb.forms import RegistrationForm, LoginForm, UpdateAccountForm, ReviewForm
from flaskweb.models import User, Review
from flaskweb import app, db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
@app.route('/home')
def home():
	page = request.args.get('page', 1, type=int)
	reviews = Review.query.order_by(Review.date_posted.desc()).paginate(page=page, per_page=5)
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

def save_picture(form_picture, w, h):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics/' + picture_fn)
	
	output_size = (int(w), int(h))
	i = Image.open(form_picture)
	i.thumbnail(output_size)

	i.save(picture_path)
	return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data, 125, 125)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Account updated successfully!', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
	return render_template('account.html', title='My Account', image_file=image_file, form = form)

@app.route('/review/new', methods=['GET', 'POST'])
@login_required
def write_review():
	form = ReviewForm()
	if form.validate_on_submit():
		review = Review(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(review)
		db.session.commit()
		flash('Review posted!', 'success')
		return redirect(url_for('home'))
	return render_template('write_review.html', title='Write Review',
							form=form, legend='Write a Review')

@app.route('/review/<int:review_id>')
def review(review_id):
	review = Review.query.get_or_404(review_id)
	return render_template('review.html', title=review.title, review=review)

@app.route('/review/<int:review_id>/update', methods=['GET', 'POST'])
@login_required
def update_review(review_id):
	review = Review.query.get_or_404(review_id)
	if review.author != current_user:
		abort(403)
	form = ReviewForm()
	if form.validate_on_submit():
		review.title = form.title.data
		review.content = form.content.data
		db.session.commit()
		flash('Review has been updated!', 'success')
		return redirect(url_for('review', review_id=review.id))
	elif request.method == 'GET':
		form.title.data = review.title
		form.content.data = review.content
	return render_template('write_review.html', title='Update Review',
							form=form, legend='Update Review')

@app.route('/review/<int:review_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_review(review_id):
	review = Review.query.get_or_404(review_id)
	if review.author != current_user:
		abort(403)
	db.session.delete(review)
	db.session.commit()
	flash('Review has been deleted!', 'info')
	return redirect(url_for('home'))

@app.route('/user/<string:username>')
def user_reviews(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	reviews = Review.query.filter_by(author=user).order_by(Review.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('user_reviews.html', title=user.username+'\'s Reviews', reviews=reviews, user=user)
