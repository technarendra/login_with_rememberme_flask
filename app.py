from flask import Flask, url_for, render_template, redirect,session, request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, UserManager, UserMixin
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user, fresh_login_required
# from urllib.parse import urlparse, urljoin
from six.moves.urllib.parse import urlparse,urljoin
from datetime import timedelta
from config import Config
import sqlite3
import datetime


app = Flask(__name__)

app.config.from_object(Config)
# all this setting is shifted to config.py and use here as ..ap.config.from_object(Config)
# app.config['SECRET_KEY'] = 'thisissecretkey'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/narendra/narendra/flask/flaskloginRemembup/database.db'
# # 'sqlite:////mnt/c/Users/antho/Documents/flaskuser/database.db'
# app.config['CSRF_ENABLED'] = True
# app.config['USER_ENABLE_EMAIL'] = False
# app.config['USE_SESSION_FOR_NEXT'] = True
# app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=90)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You can\'t access that page. You need to login first'
db = SQLAlchemy(app)


def is_safe_url(target):
	ref_url = urlparse(request.host_url)
	test_url = urlparse(urljoin(request.host_url, target))

	return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


# class User(db.Model, UserMixin):
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(50), nullable=False, unique=True)
# 	password = db.Column(db.String(255), nullable=False, server_default='')
# 	active = db.Column(db.Boolean(), nullable=False, server_default='0')
class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(10))
    email = db.Column('email',db.String(50),unique=True , index=True)
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
 
    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email
        # self.registered_on = datetime.utcnow()

    def is_authenticated(self):
    	return True

    def is_active(self):
    	return True

    def is_anonymous(self):
    	return False

    def get_id(self):
    	return (self.id)

    def __repr__(self):
    	return '<User %r>' % (self.username)








@login_manager.user_loader
def load_user(user_id):
	return User.query.get(user_id)
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.filter_by(alternative_id=user_id).first()


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		user = User.query.filter_by(username=username,password=password).first()

		if not user:
			flash('Username or Password is invalid' , 'error')
			return redirect(url_for('login'))
			# return '<h1>User does not exist</h1>'
			# if registered_user is None:
              
		login_user(user, remember=True)

		if 'next' in session:
			next = session['next']
			flash('You are logged in')
			return render_template('home.html')

			# return '<h1>You are logged in</h1>'

		if is_safe_url(next):
			return redirect(next)
			flash('You are logged in')
			return render_template('home.html')
	session['next'] = request.args.get('next')
	return render_template('login.html')


@app.route('/')
@login_required
def home():
	if 'next' in session:
		next = session['next']
		# flash('You are already logged in')
		ret = 'You are already logged in, {}!'.format(current_user.username)
		return render_template('home.html',ret = ret)
	else:
		return redirect(url_for('/login'))

		



@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You are now logged out')
	return redirect(url_for('login'))



# user_manager = UserManager(app, db, User)

# @app.route('/')
# def index():
# 	return '<h1>This is the Home Page </h1>'

# @app.route('/profile')
# # @login_required
# def profile():
# 	return '<h1>This is the protect profile page</h1>'

@app.route('/register' , methods=['GET','POST'])
def register():
	if request.method == 'POST':
		user = User(request.form['username'] , request.form['password'],request.form['email'])
		db.session.add(user)
		db.session.commit()
		flash('User successfully registered')
		return redirect(url_for('login'))
	return render_template('register.html')



if __name__ == '__main__':
	app.run(debug=True)