from flask import Flask
from flask import render_template
from flask import Response
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/')
def index():
	"""
	Returns a static page.

	The decorator @app.route('/') tells Flask which URL should trigger our
		function. In this case, '/' is our index.html
	"""
	return render_template('index.html')  # Renders index.html


@app.route('/about')
def about():
	"""Returns the about page, which for now is just index.html"""
	return render_template('about.html')


@app.route('/query')
def query():
	'''Returns a very simple query and shows it on the webpage'''
	def show_it():
		# Connect to database
		try:
			client = MongoClient('mongodb://localhost:27017/')
			print('Connection successful.')
		except:
			print('Could not connect to MongoDB')
			return


		db = client.requests  # Database
		collection = db.sr    # Collection within database
		print(
			'# of documents: ' + \
			str(
				collection.find({'Complaint Type': 'Special Enforcement'}).count()
			   )
			)

		# pymongo's 'find' returns a Cursor object that must be iterated over.
		for x in collection.find({'Complaint Type': 'Special Enforcement'}):
			yield '{}<br>\n'.format(x)

	return Response(show_it(), mimetype='text/html')

'''
To actually run this, we need to export the environment variable
"FLASK_APP", ex: export FLASK_APP=app.py
'''

if __name__ == '__main__':
	app.run()
