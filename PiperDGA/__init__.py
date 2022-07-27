from distutils.command.config import config
from distutils.command.upload import upload
from posixpath import sep
from config import Config, UploadFileForm
from .routes import creardf_piper, plot

from contextlib import redirect_stderr
from flask import Flask, render_template, request, redirect, url_for, session, Response
from flask_wtf import FlaskForm
#from requests import request as rqt
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
import pandas as pd

import matplotlib.pyplot as plt
from wqchartpy import piper
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
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
    return render_template('colorsel.html', tipografico=graficos)

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
        if request.form["Clase1"]!="Ninguno" and request.form["Clase2"] !="Ninguno":
            clasif=[("Clase1",request.form["Clase1"]),("Clase2",request.form["Clase2"])]
            session["Clas"] = dict (clasif)
        elif request.form["Clase1"]!="Ninguno" and request.form["Clase2"] =="Ninguno":
            clasif=[("Clase1",request.form["Clase1"])]
            session["Clas"] = dict (clasif)
        elif request.form["Clase2"]!="Ninguno" and request.form["Clase1"] =="Ninguno":
            clasif=[("Clase2",request.form["Clase2"])]
            session["Clas"] = dict (clasif)
        else: 
            clasif=""
            session["Clas"] = clasif
        for elm in elementos:
            llaves.append((elm,request.form[elm]))
        
            #print (request.form[elm])
        next=True
        session["llaves"]=dict(llaves)
        
        return redirect(url_for('Visor'))
        
    return render_template('carga.html',tabla=titulos,elem=elementos,cabecera='Parámetros '+tg, dtip=dtipo)

@app.route('/Grafico.jpg', methods=['GET','POST'])
def Grafico():
    dicc=session["llaves"]
    clas=session["Clas"]
    ruta=session["ruta"] 
    tit = pd.read_csv(ruta,",")
    df=tit
    print (clas)
    format_df= creardf_piper(Y_df=df,sz=30, di=dicc,cla=clas)
    filtro=''
    filtro2=''
    format_df.to_csv("formato.csv",sep=";")
    
    fig=plot(format_df, unit='mg/L', figname='Piper '+filtro+'_'+filtro2+'_Subcuenca', figformat='jpg',nc=1)
    output = io.BytesIO()
    FigureCanvas(fig).print_jpg(output)
    
    
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/Color')
def Color():
    
    return render_template('colorsel.html')



