from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskweb import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	"""user model"""
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	reviews = db.relationship('Review', backref='author', lazy=True)

	def get_reset_token(self, expiry_in_secs=1800):
		serial = Serializer(app.config['SECRET_KEY'], expiry_in_secs)
		return serial.dumps({'user_id':self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		serial = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = serial.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image_file}')"

class Review(db.Model, UserMixin):
	"""Review model"""
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Review('{self.title}', '{self.date_posted}')"