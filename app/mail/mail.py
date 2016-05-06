from flask_mail import Message, Mail
from models import app

class Email():
	app.config['MAIL_SERVER']='smtp.gmail.com'
	app.config['MAIL_PORT'] = 465
	app.config['MAIL_USERNAME'] = 'info@mradifund.com'
	app.config['MAIL_PASSWORD'] = 'Mradi_2014'
	app.config['MAIL_USE_TLS'] = False
	app.config['MAIL_USE_SSL'] = True

	mail = Mail(app)

	

	def __init__(self, re, recipients, from_add, body):
		self.re = re
		self.recipients = recipients
		self.from_add = from_add
		self.body = body

	def send_login_creds(self):
		msg = Message(self.re, self.from_add)
		msg.recipients = [self.recipients]
		msg.body = self.body
		mail.send(msg)

