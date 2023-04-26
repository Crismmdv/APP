from posixpath import sep
from config import Config
from .routes import creardf_piper, plot_piper, plot_scholler, corregir_BD,ncolran_dic


from flask import Flask, render_template, request, redirect, url_for, session, Response

#from requests import request as rqt

from werkzeug.utils import secure_filename
import os
import sys
import pandas as pd

from matplotlib.lines import Line2D


#from wqchartpy import piper
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask_cors import CORS
import jinja2


#import webview
if getattr(sys,'frozen', False):
    template_folder=os.path.join(sys._MEIPASS, os.path.normpath(Config.TEMPLATE_FOLDER))
    static_folder=os.path.join(sys._MEIPASS, os.path.normpath(Config.STATIC_FOLDER))
    upload_folder=os.path.join(sys._MEIPASS, os.path.normpath(Config.UPLOAD_FOLDER))
    # print (template_folder)
    # print (static_folder)
    loader = jinja2.FileSystemLoader(template_folder)
    environment = jinja2.Environment(loader=loader)
    loader2 = jinja2.FileSystemLoader(static_folder)
    environment2 = jinja2.Environment(loader=loader2)
    app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
else: 
    app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)
    upload_folder=Config.UPLOAD_FOLDER
app.config.from_object(Config)
CORS(app)




@app.route('/')
def principal():
    return render_template('index.html')
@app.route('/Datos', methods=['GET','POST'])
def Datos():
    if request.method=="POST":
        if request.files:
            arch =request.files['archivo']
            ruta3= os.path.join(os.path.abspath(os.path.dirname(__file__)),upload_folder, arch.filename)
            ruta2 =os.path.join(os.path.abspath(os.path.dirname(__file__)),upload_folder)
            arch.save(ruta3)
            #print (ruta3)
            try:
                if request.form['corregir']=="1": session['corregir']=True
            except:
                session['corregir']=False

            session["ruta"]=ruta3
            session["ruta2"]=ruta2
            return redirect(url_for('Tablas'))

    return render_template('Datos.html')
@app.route('/Tablas', methods=['GET','POST'])
def Tablas():
    elementos=()
    if "ruta" in session:
        ruta=session["ruta"]
        session["keys"]=''
        session["elm_ley"]=list()
        try: 
            tit = pd.read_csv(ruta, encoding='utf-8', sep=',')
            #session["CSV"]=tit
            if len(tit.columns.values[0])>30: tit = pd.read_csv(ruta, encoding='utf-8', sep=';')
            if session['corregir']: 
                tit=corregir_BD(tit)
                tit.to_csv(ruta, encoding='utf-8', sep=',')
            #print (session['corregir'])
            dtipo= tit.dtypes
            dindex=list(dtipo.index)
            dvalues=list(dtipo.values.astype(str))
            dtipo= dict( pd.Series(dvalues, index= dindex))
            #dtipo=dtipo | dict(zip(['Eliminar'],['object']))
            session['dtipo']=dtipo
        except:
            try: tit= pd.read_csv(ruta, encoding='utf-8', sep=';')
            except: tit = pd.read_csv(ruta, encoding='latin', sep=';')
            #session["CSV"]=tit
            if len(tit.columns.values[0])>30:
                try:tit = pd.read_csv(ruta, encoding='utf-8', sep=',')
                except:tit = pd.read_csv(ruta, encoding='latin', sep=',')
            if session['corregir']: 
                tit=corregir_BD(tit)
            tit.to_csv(ruta, encoding='utf-8', sep=',')
            #print (session['corregir'])
            dtipo= tit.dtypes
            dindex=list(dtipo.index)
            dvalues=list(dtipo.values.astype(str))
            dtipo= dict( pd.Series(dvalues, index= dindex))
            #dtipo=dtipo | dict(zip(['Eliminar'],['object']))
            session['dtipo']=dtipo
                
    else: titulos='error'
    
    titulos= tit.columns.values
    
    if request.method =='POST':
        
        lista_de_tabla=list()    
        
        tg= request.form['tipog']
        session["tipograf"]=tg
        if tg == "Schoeller":
            elementos = ('Al','Cu', 'Cr','F', 'Fe', 'Mn', 'Mg', 'Se', 'Zn','As','Cd','Hg','NO3','Pb','Cl','SO4','TDS')
        elif tg== "Piper":
            elementos= ('Cl','SO4','HCO3','CO3','Na','Ca','Mg','K','TDS')
        elif tg== "Gibbs":
            elementos= ('Cl','HCO3','Na','Ca','TDS')
        session["elementos"]=elementos
        
        
        next = tg!=''
        #print (dtipo)
        if next:
            return redirect(url_for('Validacion'))
        return render_template('carga.html',tabla=titulos,elem=elementos,cabecera="Error")
    return render_template('cargapiper.html',tabla=titulos,elem=elementos)   



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
    session["keys"]=''

    # Crear diccionario de colores y simbolos 
    #---------------------------------------
    ruta=session["ruta"] 
    tit = pd.read_csv(ruta, encoding='utf-8', sep=',')
    df=tit
    session["dic_col_sim"]=["",""]
    #---------------------------------------     
    if request.method=='POST':
        llaves=list()
        if request.form["Cod"]!="Ninguno":
            llaves.append(("Cod",request.form["Cod"]))
        if request.form["Clase1"]!="Ninguno" and request.form["Clase2"] !="Ninguno":
            clasif=dict([("Clase1",request.form["Clase1"]),("Clase2",request.form["Clase2"])])
            session["Clas"] = clasif
            col, simb= ncolran_dic(df,clasif) #diccionarios de col , simb
            session["dic_col_sim"]=[col,simb]
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
            if request.form[elm]=="Sup": continue
            else: llaves.append((elm,request.form[elm]))
        
        #print (llaves)
        next=True
        session["llaves"]=dict(llaves)
        
        return redirect(url_for('Visor'))
        
    return render_template('carga.html',tabla=titulos,elem=elementos,cabecera='Parámetros '+tg, dtip=dtipo)
@app.route('/Visor', methods=['GET','POST'])
def Visor():

    # Crear diccionario de colores y simbolos 
    #---------------------------------------
    ruta=session["ruta"] 
    tit = pd.read_csv(ruta, encoding='utf-8', sep=',')
    df=tit
    clasif=session["Clas"]
    #---------------------------------------
    if len(clasif)>1:     
        col, simb= ncolran_dic(df,clasif)
    session["check"]=-1
    #lista=list()
    session["elm_ley"]=list()
    graficos=("Schoeller","Piper", "Stiff")
    if request.method=='POST':
        #print ('check')
        try: 
            val=request.form["TDS_check"]
            session["check"]=1
        except: session["check"]=-1
        #session["check"]*=float(val)
        #print (session["check"])
        session["TDS"]=(session["check"]>0)
        if session["keys"]!='':
            post_sim=list()
            try:
                for h in list(simb.keys()):
                    val=request.form[h]
                    if val=='Seleccione símbolo...':
                        cont=True
                    else: cont=False
                    post_sim.append((h,val))
                if not cont:
                    session["dic_col_sim"][1]=dict(post_sim)
            except:
                val=0
            for i in session["keys"]:
                try: session["elm_ley"].append(request.form[i])
                except: continue
            
            #print ('ELM_LEY',session["elm_ley"])
        #return render_template('colorsel.html', tipografico=graficos)
    else: 
        session["TDS"]=False
        #return render_template('colorsel.html', tipografico=graficos)
    #print (session["keys"])
    if session["keys"] !="":
        grup_simb=list(simb.keys())
        simbolos=list(Line2D.filled_markers)
    else:
        grup_simb=list()
        simbolos=list()
    return render_template('colorsel.html', tipografico=graficos , check=session["TDS"], key=session["keys"], chekes=session["elm_ley"],grup_sel=grup_simb,simb=simbolos)



@app.route('/Grafico.jpg', methods=['GET','POST'])
def Grafico():
    tds=session["TDS"]
    dicc=session["llaves"]
    clas=session["Clas"]
    ruta=session["ruta"]
    dcol, dsim =tuple(session["dic_col_sim"])
    #print (dsim)
    tit = pd.read_csv(ruta, encoding='utf-8', sep=',')
    df=tit
    #print ("diccionario ",dicc)
    format_df,lyd= creardf_piper(Y_df=df,sz=50, di=dicc,cla=clas,std=tds,dict_col=dcol,dict_sim=dsim)
    filtro=''
    filtro2=''
    indexes=list(format_df.index.values)
    gb=format_df.groupby('Label_layout')
    session["keys"]=list(gb.groups.keys())
    ley=session["elm_ley"]
    filt_ley=list()
    filt_ley2=list()
    # print ('prefiltro',len(lyd), dcol.keys(), dsim.keys())
    if ley!='' and len(ley)>0:
        for i in ley:
            k=list(gb.indices[i])
            filt_ley.append(k)
        for h in filt_ley:
            filt_ley2+=h
        
        format_df=format_df.filter(items=filt_ley2, axis=0)
        rcol=format_df.groupby([clas['Clase1']]).groups.keys()
        rsim=format_df.groupby([clas['Clase2']]).groups.keys()
        bcol=[x for x in dcol.keys() if x in rcol]
        bsim=[x for x in dsim.keys() if x in rsim]
        dcol2=dict()
        dsim2=dict()
        for j in bcol: dcol2[j]=dcol[j]
        for j in bsim: dsim2[j]=dsim[j]
        _,lyd=creardf_piper(Y_df=format_df,sz=50, di=dict(),cla=clas,std=tds,dict_col=dcol2,dict_sim=dsim2)
        
        # print ('filtro',len(lyd), dcol.keys(), dsim.keys())
    #format_df.to_csv("formato.csv",sep=";")
    if session['tipograf']=='Piper': 
        fig=plot_piper(format_df, unit='mg/L', figname='Piper '+filtro+'_'+filtro2+'_Subcuenca', figformat='jpg',nc=1,lyd=lyd)
    elif session['tipograf']=='Schoeller':
        
        fig= plot_scholler(format_df, unit='mg/L', figname='Diagrama de Scholler de elementos normados', figformat='jpg',ms= 8,n=True,nch='Nch 409',lyd=lyd)
    elif session['tipograf']=='Gibbs':
        fig=''
    output = io.BytesIO()
    FigureCanvas(fig).print_jpg(output, dpi=200, quality=100)
    #os.remove(session["ruta"])
    
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/Color')
def Color():
    
    return render_template('colorsel.html')

def len_function(y):
    return len(y)

app.jinja_env.globals.update(len_function=len_function)

