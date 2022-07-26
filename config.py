from distutils.debug import DEBUG
import os
from telnetlib import ENCRYPT
from dotenv import load_dotenv
from flask_wtf import FlaskForm
#from requests import request as rqt
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired

load_dotenv()

class Config:
    SERVER_NAME = 'localhost:5000'
    DEBUG = True

    DATABASE_PATH = "Piper/database/qca.db"
    DB_TOKEN = os.environ.get("DB_TOKEN","")
    ENCRYPT_DB=True

    TEMPLATE_FOLDER ="views/templates/"
    STATIC_FOLDER = "views/statics/"

    SECRET_KEY ='botonsecreto'
    UPLOAD_FOLDER='static/cargas'

class UploadFileForm(FlaskForm):
    file= FileField("File", validators=[InputRequired()])
    submit= SubmitField("Upload File")


