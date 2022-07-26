from distutils.command.config import config
from distutils.command.upload import upload
from config import Config, UploadFileForm
from .routes import plotpiper, creardf_piper

from contextlib import redirect_stderr
from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from flask_wtf import FlaskForm
#from requests import request as rqt
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import pandas as pd

import matplotlib.pyplot as plt



app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)
app.config.from_object(Config)


@app.route('/')
def principal():
    return render_template('index.html')
@app.route('/Datos', methods=['GET','POST'])
def Datos():
    if request.method=="POST":
        if request.files:
            arch =request.files['archivo']
            ruta3= os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config["UPLOAD_FOLDER"], arch.filename)
            ruta2 =os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config["UPLOAD_FOLDER"])
            arch.save(ruta3)
            #print (ruta3)

            session["ruta"]=ruta3
            session["ruta2"]=ruta2
            return redirect(url_for('Tablas'))

    return render_template('Datos.html')
@app.route('/Tablas', methods=['GET','POST'])
def Tablas():
    elementos=()
    if "ruta" in session:
        ruta=session["ruta"] 
        try: 
            tit = pd.read_csv(ruta)
            #session["CSV"]=tit
            dtipo= tit.dtypes
            dindex=list(dtipo.index)
            dvalues=list(dtipo.values.astype(str))
            dtipo= dict( pd.Series(dvalues, index= dindex))
            session['dtipo']=dtipo
        except: titulos=''
    else: titulos='error'
    titulos= tit.columns.values
    if request.method =='POST':
        
        lista_de_tabla=list()    
        
        tg= request.form['tipog']
        session["tipograf"]=tg
        if tg == "Schoeller":
            elementos = ('Cu', 'Cr','F', 'Fe', 'Mn', 'Mg', 'Se', 'Zn','As','Cd','Hg','NO3','Pb','Cl','SO4','TDS')
        elif tg== "Piper":
            elementos= ('Cl','SO4','HCO3','CO3','Na','Ca','Mg','K')
        elif tg== "Gibbs":
            elementos= ('Cl','HCO3','Na','Ca','TDS')
        session["elementos"]=elementos
        
        
        next = tg!=''
        #print (dtipo)
        if next:
            return redirect(url_for('Validacion'))
        return render_template('carga.html',tabla=titulos,elem=elementos,cabecera="Error")
    return render_template('cargapiper.html',tabla=titulos,elem=elementos)   


@app.route('/Visor')
def Visor():
    graficos=("Schoeller","Piper", "Stiff")
    return render_template('visor.html', tipografico=graficos)

@app.route('/Prueba')
def Prueba():
    

    if request.method =='POST':
        elementos=session["elementos"]

                            
        return render_template('clear.html')
    return redirect(url_for('Visor'))

def new_func():
    lista_de_tablas=list()

@app.route('/Validacion', methods=['GET','POST'])
def Validacion():
    elementos=session["elementos"]
    
    titulos= list(session["dtipo"].keys())
    dtipo= session["dtipo"]
    tg=session["tipograf"]
    session["tipograf"]=tg
            
    if request.method=='POST':
        llaves=list()
        for elm in elementos:
            llaves.append((elm,request.form[elm]))
            #print (request.form[elm])
        next=True
        session["llaves"]=dict(llaves)
        return redirect(url_for('Grafico'))
        
    return render_template('carga.html',tabla=titulos,elem=elementos,cabecera='Parámetros '+tg, dtip=dtipo)

@app.route('/Grafico', methods=['GET','POST'])
def Grafico():
    dicc=session["llaves"]
    
    ruta=session["ruta"] 
    tit = pd.read_csv(ruta)
    df=tit
    format_df= creardf_piper(Y_df=df,sz=25, di=dicc)
    filtro=''
    filtro2=''
    dir=session["ruta2"]
    img1=plotpiper(format_df, unit='mg/L', figname='Piper '+filtro+'_'+filtro2+'_Subcuenca', figformat='jpg',nc=1)
    img=(os.path.join("C:\Users\cristobal.machuca\OneDrive - ug.uchile.cl\App piper" ,img1))
    print (img)
    return render_template('clear.html',df=img)





