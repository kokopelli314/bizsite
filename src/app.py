from decouple import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, request
import urllib.request
import smtplib
from typing import NamedTuple, Union
from wtforms import Form, StringField, validators, TextAreaField

app = Flask(__name__)


@app.route('/')
def homepage():
	return render_template('index.html')

@app.route('/about')
def about_us():
	return render_template('about.html')

@app.route('/contact', defaults={'email_address': None}, methods=['get'])
@app.route('/contact/<string:email_address>', methods=['get'])
def contact(email_address):
	if email_address:
		request.form.email_address = email_address
	form = ContactForm(request.form, email_address=email_address)
	return render_template('contact.html', form=form)

@app.route('/contact', methods=['post'])
def contact_send_message():
	"""Send a message from the contact form."""
	form = ContactForm(request.form)
	success = False
	if form.validate():
		success = True
		sendEmail(form)
	user_message = (
		'Your message was sent successfully! Thank you.' if success
		else 'An error occurred while trying to send your message. Please try again later, or contact us directly by email or phone.'
	)
	return render_template('contact.html', form=form, user_message=user_message)


class ContactForm(Form):
	name = StringField('Name', [validators.DataRequired()])
	email_address = StringField('Email Address', [validators.DataRequired()])
	business_name = StringField('Business Name (optional)', [])
	phone_number = StringField('Phone Number (optional)', [])
	message = TextAreaField('Message', [validators.DataRequired()])

def sendEmail(submission: ContactForm):
	host = config('SMTP_HOST')
	port = config('SMTP_PORT')
	username = config('SMTP_USERNAME')
	password = config('SMTP_PASSWORD')
	sender = config('EMAIL_FROM')
	receivers = submission.email_address.data

	msg = MIMEMultipart()
	msg['From'] = sender
	msg['To'] = receivers
	msg['Subject'] = 'Clonts Software Development Message - %s' % submission.name.data

	body = """
	New contact form message:
	Name: %s
	Email Address: %s
	Business Name: %s
	Phone Number: %s
	Message: %s
	""" % (
		submission.name.data,
		submission.email_address.data,
		submission.business_name.data,
		submission.phone_number.data,
		submission.message.data,
	)
	msg.attach(MIMEText(body))

	try:
		server = smtplib.SMTP_SSL(host, port)
		server.ehlo()
		server.login(username, password)
		server.sendmail(sender, receivers, msg.as_string())
		server.close()
	except Exception as e:
		print(e)
