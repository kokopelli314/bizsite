from flask import Flask, render_template
app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def homepage():
	return render_template('index.html')

@app.route('/contact')
def contact():
	return ''
