import uuid
import logging
from flask import Flask, render_template, request
from flask_session_captcha import FlaskSessionCaptcha
from flask_session import Session
from pymongo import MongoClient

# Create a Flask web server
app = Flask(__name__, template_folder='templates')  # Assuming 'templates' is the correct folder

# Connect to MongoDB
mongoClient = MongoClient('localhost', 27017)

# Configure Flask app settings
app.config['SECRET_KEY'] = str(uuid.uuid4())  # Generate a secret key for CSRF protection
app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 5
app.config['CAPTCHA_WIDTH'] = 160
app.config['CAPTCHA_HEIGHT'] = 60
app.config['SESSION_MONGODB'] = mongoClient  # Specify the MongoDB client instance
app.config['SESSION_TYPE'] = 'mongodb'  # Set the session type to MongoDB

# Get the database and collection references
db = mongoClient['local']  # Use 'local' database
collection = db['Collection']  # Reference to the 'Collection' collection

# Initialize Flask-Session with MongoDB
Session(app)

# Initialize FlaskSessionCaptcha
captcha = FlaskSessionCaptcha(app)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if captcha.validate():
            return 'success'
        else:
            return 'fail'
    return render_template('form.html')  # Render the form template

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)  # Set log level to DEBUG for detailed logs
    app.run(debug=True)  # Run the Flask app in debug mode