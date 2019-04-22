from decouple import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template
import urllib.request
import smtplib
from typing import NamedTuple

app = Flask(__name__)


@app.route('/')
def homepage():
	return render_template('index.html')


@app.route('/contact', defaults={'email_address': None})
@app.route('/contact/<string:email_address>')
def contact(email_address):
	print(email_address)
	return render_template('contact.html', email_address=email_address)


class ContactFormSubmission(NamedTuple):
	email_address: str
	message: str
	name: str
	business_name: str | None
	phone_number: str | None
	timestamp: any

def sendEmail(submission: ContactFormSubmission):
	host = config('SMTP_HOST')
	port = config('SMTP_PORT')
	username = config('SMTP_USERNAME')
	password = config('SMTP_PASSWORD')
	sender = config('EMAIL_FROM')
	receivers = submission.email_address

	msg = MIMEMultipart()
	msg['From'] = sender
	msg['To'] = receivers
	msg['Subject'] = 'Clonts Software Development Message - %s' % submission.name

	body = """
	New contact form message:
	Name: %s
	Email Address: %s
	Business Name: %s
	Phone Number: %s
	Message: %s
	""" % (
		submission.name,
		submission.email_address,
		submission.business_name,
		submission.phone_number,
		submission.message,
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
