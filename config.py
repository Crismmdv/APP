import os
#from dotenv import load_dotenv
from flask_wtf import FlaskForm
#from requests import request as rqt
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired


#load_dotenv()

class Config:
    SERVER_NAME = 'localhost:5000'
    DEBUG = False

    DATABASE_PATH = "Piper/database/qca.db"
    DB_TOKEN = os.environ.get("DB_TOKEN","")
    ENCRYPT_DB=True

    TEMPLATE_FOLDER ="views/templates/"
    STATIC_FOLDER = "views/static/"

    SECRET_KEY ='botonsecreto'
    UPLOAD_FOLDER='views/static/cargas/'
    IMAGES_UPLOAD= "C:/Users/cristobal.machuca/OneDrive - ug.uchile.cl/App piper/PiperDGA/views/static/images/uploads/"

class UploadFileForm(FlaskForm):
    file= FileField("File", validators=[InputRequired()])
    submit= SubmitField("Upload File")


