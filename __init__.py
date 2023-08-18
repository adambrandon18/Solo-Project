from flask import Flask


UPLOAD_FOLDER = '/Users/Adam C/OneDrive/Documents/Projects_Algorithms/AmericanMuscleCarClub/flask_app/static/uploads'


app = Flask(__name__)


app.secret_key = "quiet!!!"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

