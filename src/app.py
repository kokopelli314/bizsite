from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template('index.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')
