import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('journal.db')


class User(UserMixin, Model):
	username = CharField(unique=True)
	email = CharField(unique=True)
	password = CharField(max_length=100)
	joined_at = DateTimeField(default=datetime.datetime.now)
	is_admin = BooleanField(default=False)

	class Meta:
		database = DATABASE
		order_by = ('-joined_at',)

	def get_journals(self):
		return Journal.select().where(Journal.user == self)
		
	@classmethod
	def create_user(cls, username, email, password, admin=False):
		try:
			cls.create(
				username=username,
				email=email,
				password=generate_password_hash(password),
				is_admin=admin)
		except IntegrityError:
			raise ValueError("User already exists")	
		

class Journal(Model):
	title = CharField(max_length=100)
	date = DateTimeField(default=datetime.datetime.now)
	time_spent = IntegerField()
	what_i_learned = TextField()
	to_remember = TextField()
	user = ForeignKeyField(
		rel_model=User,
		related_name='journals')

	class Meta:
		database = DATABASE
		order_by = ('-date',)


def initialize():
	DATABASE.connect(),
	DATABASE.create_tables([Journal, User], safe=True)
	DATABASE.close()		