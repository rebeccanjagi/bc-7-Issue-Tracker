
from sqlalchemy import Column, Integer, String
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, g, jsonify
from sqlalchemy import exc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DR56$%6jnbix586wEr'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///issuertracker.db'
db = SQLAlchemy(app)

class Account(db.Model):
	__tablename__ = 'accounts'

	id = db.Column(db.Integer, primary_key=True)
	org_id = db.Column(db.String(50), unique=True)
	f_name = db.Column(db.String(50))
	l_name = db.Column(db.String(50))
	department = db.Column(db.String(50))
	password = db.Column(db.String(200))
	email = db.Column(db.String(50), unique=True)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	active = db.Column(db.String(10), default="Yes")
	user_type = db.Column(db.String(50), default="user")

	def __init__(self, org_id=None, f_name=None, l_name=None, department=None, password=None, email=None):
		self.org_id = org_id
		self.f_name = f_name
		self.l_name = l_name
		self.department = department
		self.email = email
		self.password = password
		self.active = "Yes"
		self.user_type = "user"

	

	def __repr__(self):
	    return self.f_name
	


class Employee(db.Model):
	__tablename__ = 'employees'

	id = db.Column(db.Integer, primary_key=True)
	org_id = db.Column(db.String(50), db.ForeignKey('accounts.org_id'), unique=True)
	department = db.Column(db.String(50))
	f_name = db.Column(db.String(50))
	l_name = db.Column(db.String(50))
	email = db.Column(db.String(50), unique=True)

	def __init__(self, org_id=None, department=None, f_name=None, l_name=None, email=None):
		self.org_id = org_id
		self.department = department
		self.f_name = f_name
		self.l_name = l_name
		self.email = email

	def __repr__(self):
	    return '<Employee %r>' % (self.department)


class Issue(db.Model):
	__tablename__ = 'issues'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(50))
	description = db.Column(db.Text)
	priority = db.Column(db.String(10))
	department = db.Column(db.String(50))
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	status = db.Column(db.String(50))
	date_resolved = db.Column(db.DateTime)
	assigned_to = db.Column(db.String(50))
	raised_by = db.Column(db.String(50))
	deadline = db.Column(db.DateTime)
	percentage_completed = db.Column(db.String(20))
	solution = db.Column(db.Text)

	def __init__(self, title, description, priority, department, status, date_resolved, assigned_to, raised_by, deadline, percentage_completed,solution=None):
		self.title = title
		self.description = description
		self.priority = priority
		self.department = department
		self.status = status
		self.date_resolved = date_resolved
		self.assigned_to = assigned_to
		self.raised_by = raised_by
		self.deadline = deadline
		self.percentage_completed = percentage_completed
		self.solution = solution


	# def __repr__(self):
	# 	return jsonify({'title': self.title, 'description': self.description})
		# return jsonify([self.title, self.description, self.priority, self.department, self.status, self.date_resolved, self.assigned_to, self.raised_by, self.deadline])

class Note(db.Model):
	__tablename__ = 'notes'

	id = db.Column(db.Integer, primary_key=True)
	issue_id = db.Column(db.String(50), db.ForeignKey('issues.id'))
	description = db.Column(db.Text)
	sender_id = db.Column(db.String(50))
	receiver_id = db.Column(db.String(50))
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

	def __init__(self, issue_id=None, description=None, sender_id=None, receiver_id=None, date_created=None):
		self.issue_id = issue_id
		self.description = description
		self.sender_id = sender_id
		self.receiver_id = receiver_id
		self.date_created = date_created

	def __repr__(self):
	    return '<Note %r>' % (self.description)

class Resolution(db.Model):
	__tablename__ = 'resolutions'

	id = db.Column(db.Integer, primary_key=True)
	issue_id = db.Column(db.String(50), db.ForeignKey('issues.id'))
	description = db.Column(db.Text)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

	def __init__(self, issue_id=None, description=None, date_created=None):
		self.issue_id = issue_id
		self.description = description
		self.date_created = date_created

	def __repr__(self):
	    return '<Resolution %r>' % (self.description)

class Priority(db.Model):
	__tablename__ = 'priorities'

	id = db.Column(db.Integer, primary_key=True)
	priority = db.Column(db.String(50))
	days = db.Column(db.Integer)

	def __init__(self, priority=None, days=None):
		self.priority = priority
		self.days = days

	def __repr__(self):
	    return '<Priority %r>' % (self.priority)

class Email(db.Model):
	__tablename__ = 'emails'

	id = db.Column(db.Integer, primary_key=True)
	re = db.Column(db.String(50))
	body = db.Column(db.Text)
	from_address = db.Column(db.String(50))
	to_address = db.Column(db.String(50))
	cc_address = db.Column(db.String(50))
	status = db.Column(db.String(20))
	date_sent = db.Column(db.DateTime, default=db.func.current_timestamp())

	def __init__(self, re=None, body=None, from_address=None, to_address=None, cc_address=None, status=None, date_sent=None):
		self.re = re
		self.body = body
		self.from_address = from_address
		self.to_address = to_address
		self.cc_address = cc_address
		self.status = status
		self.date_sent = date_sent

	def __repr__(self):
	    return '<Email %r>' % (self.re)

