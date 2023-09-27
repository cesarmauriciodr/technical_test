from flask import Flask
import settings

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.config['UPLOAD_FOLDER'] = settings.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = settings.MAX_CONTENT_LENGTH

