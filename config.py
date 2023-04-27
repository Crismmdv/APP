import os
#from dotenv import load_dotenv
from flask_wtf import FlaskForm
#from requests import request as rqt
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired


#load_dotenv()

class Config:
    SERVER_NAME = 'localhost.localdomain'
    DEBUG = False

    
    TEMPLATE_FOLDER ="views/templates/"
    STATIC_FOLDER = "views/static/"

    SECRET_KEY ='botonsecreto'
    UPLOAD_FOLDER='views/static/cargas/'
    
class UploadFileForm(FlaskForm):
    file= FileField("File", validators=[InputRequired()])
    submit= SubmitField("Upload File")


