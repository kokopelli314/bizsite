from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template('index.html')


@app.route('/contact', defaults={'email_address': None})
@app.route('/contact/<string:email_address>')
def contact(email_address):
	print(email_address)
	return render_template('contact.html')
