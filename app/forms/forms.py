from flask_wtf import Form
from wtforms import StringField, validators, SelectField, PasswordField


class SignUp(Form):

	org_id = StringField(u'Organisation Id', validators=[validators.input_required()])
	f_name = StringField(u'First Name', validators=[validators.input_required()])
	l_name  = StringField(u'Last Name', validators=[validators.input_required()])
	password = PasswordField(u'Password', validators=[validators.input_required()])
	email = StringField(u'Email Address', validators=[validators.input_required(),validators.Email()])
	DEPS = [('technical','Technical'),('service','Service'),('operations','Operations')]
	department  = SelectField(u'Department', validators=[validators.input_required()],choices = DEPS)

class SignIn(Form):

	org_id = StringField(u'Organisation Id', validators=[validators.input_required()])
	password = PasswordField(u'Password', validators=[validators.input_required()])




