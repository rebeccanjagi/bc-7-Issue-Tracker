from flask import Flask, render_template, url_for, redirect, flash, session, request
from flask.ext.sqlalchemy import SQLAlchemy
from models import app, Account, db, Issue
from forms.forms import SignUp, SignIn
from validate_email import validate_email
from sqlalchemy import exc
from flask_mail import Mail, Message
from mail.mail import Email
import datetime 
from flask.ext.login import current_user

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'info@mradifund.com'
app.config['MAIL_PASSWORD'] = 'Mradi_2014'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
@app.route("/", methods=['GET', 'POST'])
def main():
	form = SignIn()
	return render_template('sign_in.html', form=form)

@app.route('/sign-up', methods=['GET', 'POST'])
def signup():
	form = SignUp()
	return render_template('/auth/sign_up.html', form=form)

@app.route('/register_users', methods=['POST'])
def registerusers():
	form = SignUp()
	org_id = request.form['org_id']
	f_name = request.form['f_name']
	l_name = request.form['l_name']
	department = request.form['department']
	password = request.form['password']
	email = request.form['email']

	accounts = Account(org_id, f_name, l_name, department, password, email)

	is_valid = validate_email(email)
	if is_valid:
		if accounts is not None:
			try:
				db.session.add(accounts)
				db.session.commit()
			except exc.SQLAlchemyError:
				flash("Your Org id. or email address is already in use")
				return render_template('/auth/sign_up.html', form=form)
			body = "Dear " + f_name + " " + l_name + ",<br /><br />Thanks for signing with  Issue Tracker.<br />Your login credentials are : <br />Organisation id : "+org_id+" <br /> Password :"+password+".<br /><br /> \
								Thanks and Kind Regards,<br /> Admin. "
			msg = Message("Issue Tracker Account Creation", sender="rebeccagathegu@gmail.com", recipients=[str(email)])
			msg.html = body
			mail.send(msg)
			flash("Your account has been successfully created. An email has been sent to you. Please login.")
			return redirect('/')
		else:
			flash("Your account has not been created.")
			return render_template('/auth/sign_up.html', form=form)
	else:
		flash("Your email address is invalid")
		return render_template('/auth/sign_up.html', form=form)
	


@app.route('/portal', methods=['POST'])
def signin():
	form = SignIn()
	org_id = request.form['org_id']
	password = request.form['password']
	verified = Account.query.filter_by(password=form.password.data).first()
	if verified is not None:

		session['org_id'] = request.form['org_id']
		details = Account.query.filter_by(org_id=org_id).first()
		session['org_id'] = details.org_id
		session['f_name'] = details.f_name
		session['l_name'] = details.l_name
		session['department'] = details.department
		session['email'] = details.email
		session['user_type'] = details.user_type

		if session['user_type'] == "user":
			open_issues = Issue.query.filter_by(status="Open", assigned_to=session['org_id']).all()
			closed_issues = Issue.query.filter_by(status="Closed").all()
			pending_issues = Issue.query.filter_by(status="Pending Assignment", raised_by=session['org_id']).all()
		
		else:
			open_issues = Issue.query.filter_by(status="Open").all()
			closed_issues = Issue.query.filter_by(status="Closed").all()
			pending_issues = Issue.query.filter_by(status="Pending Assignment", department=session['department']).all()

		return render_template('/issues/dashboard.html', form=form, open=len(open_issues), close=len(closed_issues), pending=len(pending_issues))
	flash('Invalid username or password.')
	return render_template('sign_in.html', form=form)

@app.route('/dashboard')
def dashboard():
	if session['user_type'] == "user":
		open_issues = Issue.query.filter_by(status="Open", assigned_to=session['org_id']).all()
		closed_issues = Issue.query.filter_by(status="Closed").all()
		pending_issues = Issue.query.filter_by(status="Pending Assignment", raised_by=session['org_id']).all()
		
	else:
		open_issues = Issue.query.filter_by(status="Open").all()
		closed_issues = Issue.query.filter_by(status="Closed").all()
		pending_issues = Issue.query.filter_by(status="Pending Assignment", department=session['department']).all()
	return render_template('/issues/dashboard.html', open=len(open_issues), close=len(closed_issues), pending=len(pending_issues))
	

@app.route('/raise_issue')
def raiseissue():
	return render_template('/issues/raise_issue.html')

@app.route('/log_issue',methods=['POST'])
def logissue():
	title = request.form['title']
	description = request.form['description']
	priority = request.form['priority']
	department = request.form['department']
	status = "Pending Assignment"
	date_resolved = None
	assigned_to = ""
	raised_by  = session['org_id']

	now = datetime.datetime.now()
	if priority == "High":
		end_date = now + datetime.timedelta(days=10)
	elif priority == "Medium":
		end_date = now + datetime.timedelta(days=20)
	else:
		end_date = now + datetime.timedelta(days=30)

	deadline = end_date
	percentage_completed = 0

	issue = Issue(title, description, priority, department, status, date_resolved, assigned_to, raised_by, deadline, percentage_completed)
	if issue is not None:
		try:
			db.session.add(issue)
			db.session.commit()
		except exc.SQLAlchemyError:
			flash("Unable to save the issue raised. Please contact the Admin.")
			return render_template('/issues/raise_issue.html')

		flash("Your Issue has been logged in pending assignment to a resource.")
		return render_template('/issues/raise_issue.html')
	else:
		flash("Unable to save the issue raised. Please contact the Admin.")
		return render_template('/issues/raise_issue.html')
	

@app.route('/open_issues')
def openissues():
	if session['user_type'] == "user" :
		data = Issue.query.filter_by(assigned_to = session['org_id'], status ="Open").all()
	else:
		data = Issue.query.filter_by(department = session['department'], status="Open").all()
	return render_template('/reports/open_issues_rpt.html', data=data)

@app.route('/closed_issues')
def closedissues():
	data = Issue.query.filter_by(status="Closed").all()
	return render_template('/reports/closed_issues_rpt.html',data=data)

@app.route('/pending_issues')
def pendingissues():
	if session['user_type'] == "user" :
		data = Issue.query.filter_by(raised_by = session['org_id'], status="Pending Assignment").all()
	else:
		data = Issue.query.filter_by(department = session['department'], status="Pending Assignment").all()
	return render_template('/issues/pending_issues.html', data=data)

@app.route('/update_issue/<int:x>')
def updateissues(x):
	data = Issue.query.filter_by(id=x).first()
	data2 = Account.query.filter_by(department=data.department).all()
	return render_template('/issues/update_issue.html',data=data, data2=data2)

@app.route('/detailed_close/<x>')
def detailedclose(x):
	data = Issue.query.filter_by(id=x).first()
	return render_template('/reports/detailed_closed.html',data=data)

@app.route('/assign_issues/<int:x>')
def assignissues(x):
	data = Issue.query.filter_by(id=x).first()
	data2 = Account.query.filter_by(department=data.department).all()
	return render_template('/issues/assign_issues.html', data=data, data2=data2)

@app.route('/assign_resource/<x>', methods=['POST'])
def assignresource(x):
	org_id = request.form['employee']
	row_data = Issue.query.filter_by(id=x).first()
	row_data.assigned_to = org_id
	row_data.status = "Open"
	db.session.commit()
	raised_by = Account.query.filter_by(org_id=row_data.raised_by).first()
	resource = Account.query.filter_by(org_id=org_id).first()
	body = "Dear " + resource.f_name + " " + resource.l_name + ",<br /><br />Thanks for using Issue Tracker.<br />Please note that you have been assigned an issue to resolve. Please find the details on the portal. <br /><br /> \
								Thanks and Kind Regards,<br /> Admin. "
	msg = Message("Issue Tracker Notification", sender="rebeccagathegu@gmail.com", recipients=[str(resource.email)])
	msg.add_recipient(str(raised_by.email))
	msg.html = body
	mail.send(msg)
	flash("Assignment successful.")
	return render_template('/reports/open_issues_rpt.html')

@app.route('/mark_issue_closed/<x>', methods=['POST'])
def markissueclosed(x):
	now = datetime.datetime.now()
	comment = request.form['comment']
	row_data = Issue.query.filter_by(id=x).first()
	row_data.solution = comment
	row_data.status = "Closed"
	row_data.date_resolved = now
	db.session.commit()
	raised_by = Account.query.filter_by(org_id=row_data.raised_by).first()
	resource = Account.query.filter_by(org_id=row_data.assigned_to).first()
	body = "Dear " + raised_by.f_name + " " + raised_by.l_name + ",<br /><br />Thanks for using Issue Tracker.<br />An issue you raised has been closed. Please find the details on the portal. <br /><br /> \
								Thanks and Kind Regards,<br /> Admin. "
	msg = Message("Issue Tracker Notification", sender="rebeccagathegu@gmail.com", recipients=[str(resource.email)])
	msg.add_recipient(str(raised_by.email))
	msg.html = body
	mail.send(msg)

	flash("Issue successful closed.")
	return render_template('/reports/closed_issues_rpt.html')

@app.route('/emails')
def emails():
	return render_template('/reports/emails.html')

@app.route('/logout')
def logout():
    session.pop('org_id', None)
    return redirect(url_for('main'))


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html', title="403 Error"), 403

@app.errorhandler(400)
def forbidden(error):
    return render_template('400.html', title="400 Error"), 400

@app.errorhandler(405)
def forbidden(error):
    return render_template('405.html', title="405 Error"), 405

if __name__ == "__main__":
	app.run(debug=True)