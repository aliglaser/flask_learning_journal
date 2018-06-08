from flask import (Flask, g, flash, render_template, 
					redirect, url_for, abort, request)

from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, 
						logout_user, login_required, current_user)


import models
import forms


DEBUG = True
HOST = '0.0.0.0'
PORT = 8000

app = Flask(__name__)
app.secret_key="#$ADF<Z>A@/!#rkah&aZ##zkfHJZjj99Hjhkfhgf.S/"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None	


@app.before_request
def before_request():
	"""Connect to the database before each request."""
	g.db = models.DATABASE
	g.db.connect()
	g.user = current_user


@app.after_request
def after_request(response):
	"""Close the database connection after each request"""
	g.db.close()
	return response


@app.route('/register', methods=('GET', 'POST'))
def register():
	"""Register a new user"""
	form = forms.RegisterForm()
	if form.validate_on_submit():
		flash("Yay, you registered!", "success")
		models.User.create_user(
			username=form.username.data,
			email=form.email.data,
			password=form.password.data
		)
		return redirect(url_for('list'))
	return render_template('register.html', form=form)	


@app.route('/login', methods=('GET', 'POST'))
def login():
	form = forms.LoginForm()
	if form.validate_on_submit():
		try:
			user = models.User.get(models.User.email == form.email.data)
		except models.DoesNotExist:
			flash("Your email or password doesn't match", "error")
		else:
			if check_password_hash(user.password, form.password.data):
				login_user(user)
				flash("You've been logged in!", "success")
				return redirect(url_for('list'))
			else:
				flash("Your email or password doesn't match!", "error")
	return render_template('login.html', form=form)						

@app.route('/')
@app.route('/entries')
def list():
	entries = models.Journal.select().limit(100)
	return render_template('index.html', entries=entries)


@app.route('/add', methods=('GET', 'POST'))
@login_required
def add():
	form = forms.JournalForm()
	if form.validate_on_submit():
		flash("You logged another entry :D", "success")
		print("akjkka")
		models.Journal.create(
			title = form.title.data,
			date = form.date.data,
			time_spent = form.time_spent.data,
			what_i_learned = form.what_i_learned.data,
			to_remember = form.to_remember.data,
			user=g.user._get_current_object())
		return redirect(url_for('list'))
	return render_template('new.html', form=form)	


@app.route('/entries/<int:id>')
def detail(id=None):
	entry = models.Journal.select().where(models.Journal.id == id).get()
	return render_template("detail.html", entry=entry)



@app.route('/entries/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id=None):
	entry = models.Journal.select().where(models.Journal.id == id).get()
	form = forms.JournalForm()
	if form.validate_on_submit():
		entry.title = form.title.data
		entry.date = form.date.data
		entry.time_spent = form.time_spent.data
		entry.what_i_learned = form.what_i_learned.data
		entry.to_remember = form.to_remember.data
		entry.save()
		flash("Journal entry has been updated!")
		return redirect(url_for('detail', id=entry.id, entry=entry))
	return render_template('edit.html', form=form, entry=entry)


@app.route('/entries/delete/<int:id>')
@login_required
def delete(id):
	"""Delete a journal entry."""
	try:
		entry = models.Journal.select().where(models.Journal.id == id).get()
	except models.DoesNotExist:
		abort(404)
	else:
		entry.delete_instance()
		flash("Journal entry has been deleted!", "success")
	return redirect(url_for('list'))


if __name__ == '__main__':
	models.initialize()
	try:
		models.User.create_user(
			username='nurijeon',
			email='nooti77@nate.com',
			password='password',
			admin=True
		)
	except:
		pass	
	app.run(debug=DEBUG, host=HOST, port=PORT)





