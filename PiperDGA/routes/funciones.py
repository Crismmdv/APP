# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import random as rm

import random
import random as rm
import itertools
# Graficos
import pandas as pd


import numpy as np

import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import matplotlib.cm as cm
from matplotlib.lines import Line2D

import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import matplotlib.lines as mlines

#import probscale
from decimal import Decimal
from datetime import datetime as dt

import datetime

def func_tilde(x):
    di={'Limari':'Limarí', 'Rio':'Río', 'Fuera':'F.A.E','Campana':'Campaña','Vina':'Viña','Caren':'Carén','quebrada':'Quebrada','Guatulame':'Cogotí'}
    a=x.split(' ')
    b=''
    c=0
    for i in range(len(a)):
        if i==0: a[i]=a[i][0].upper()+a[i][1:]
        if c==0: s=''
        else:s=' '
        try: 
            b+=s+di[a[i]]
            c+=1
        except: 
            b+= s+a[i]
            c+=1
    return b

def func(xx, pos):  # formatter function takes tick label and tick position
    if xx<0:
        x=-xx
    else: x=xx
    s = '%d' % x
    
    xsi=Decimal(str(x))%1 
        
    if xsi != Decimal(str(0)):
        
        if len(str(xsi))>5 and (Decimal(xsi)-Decimal(str(xsi)[:-1]))<Decimal('0.0000000000001'):
            xsi=float(Decimal(str(xsi)[:-1]))
            if xsi != 0: coma, dc=(',',str(xsi))
        else: coma, dc=(',',str(xsi))
    else:
        coma, dc= ('','')
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    if xx<0: return '-'+s + '.'.join(reversed(groups))+coma+dc[2:]   
    else: return s + '.'.join(reversed(groups))+coma+dc[2:]

def creardf_piper(Y_df,sz=60, di=dict(),cla="",std=False, dict_col="", dict_sim=""):
    format_df = pd.DataFrame()
    #filtro='F.A.E'
    #filtro2=''
    diccion=di
    if diccion== dict():
        format_df=Y_df
    else:
        for i in diccion.keys():
            #print (Y_df.columns.values)
            format_df[i]=Y_df[diccion[i]].copy()
        for h in [cla[x] for x in cla.keys()]:
            format_df[h]=Y_df[h]  
        
    if cla=="":
        format_df['Label'] = "Muestras"
        format_df['Color'] = "gray"
        format_df['Marker'] = "o"
    elif len(cla)==2:
        
        simbolos=list(Line2D.markers.keys())
        simbolos.remove(',')
        clases1=list(Y_df.groupby([cla["Clase1"]]).groups.keys())
        clases2=list(Y_df.groupby([cla["Clase2"]]).groups.keys())
        colores=ncolorandom(len(clases1))
        #print (colores)            
        if dict_col=="" and dict_sim=="":
            dict_col, dict_sim=ncolran_dic(Y_df,cla)
        lyd=leyenda_2S(cla,dic_mar=dict_sim, dic_tmp=dict_col)
    
        y_seven = Y_df[cla['Clase1']].copy()
        y_t = Y_df[cla['Clase2']].copy()
        
        for i in clases1:
            
            format_df.loc[y_seven==i, 'Color'] = '#%02x%02x%02x' % (int(dict_col[i][0][0]*255),int(dict_col[i][0][1]*255),int(dict_col[i][0][2]*255))
        for i in clases2:
            format_df.loc[y_t==i, 'Marker'] = dict_sim[i]
        
        try:
            for idx in Y_df.index: 
                date=Y_df.at[idx,cla['Clase1']]
                Y_df.at[idx,'fecha1']=dt.strptime(date, "%d-%m-%Y %H:%M:%S")
                Y_df.at[idx,'Lb']=conv_fecha(Y_df.at[idx,'fecha1'])
                Y_df.at[idx,'Lb2']=conv_fecha(Y_df.at[idx,'fecha1'],v=False)
            format_df['Label'] =((Y_df[cla['Clase2']])) +' / '+(Y_df['Lb'])
            format_df['Label_layout']= ((Y_df[cla['Clase2']]))+' / '+ (Y_df['Lb2'])  
            #print (format_df.loc[Y_df[cla['Clase2']]=='HA01','Marker'])
            
        except: 
            format_df['Label'] = (Y_df[cla['Clase1']])+' / '+((Y_df[cla['Clase2']]))
            format_df['Label_layout']= format_df['Label']
            #simbolos =["D","d","o","s","v"]
            
        
    elif len(cla)==1:
        for i in cla.keys():
            if i == "Clase1":
                colores=['red','darkorange','lime','darkviolet','blue','cyan','pink','olive','mediumpurple','blueviolet',
                    'gold','gray','black','white','green','gray','magenta','skyblue', 'indigo','purple','brown','indigo','darkcyan']
                #simbolos =["s","o","v","d","*"]

                format_df['Label'] = (Y_df[cla['Clase1']])#+' / '+((Y_df[cla['Clase2']]))
                
                clases1=list(Y_df.groupby([cla["Clase1"]]).groups.keys())
                #clases2=list(Y_df.groupby([cla["Clase2"]]).groups.keys())
                dict_col=dict(zip(clases1,colores))
                #dict_sim=dict(zip(clases2,simbolos))

                y_seven = Y_df[cla['Clase1']].copy()
                #y_t = Y_df['Clase2'].copy()
                for i in clases1:
                    format_df.loc[y_seven==i, 'Color'] = dict_col[i]
                format_df['Marker'] = 'o'
            else:
                
                simbolos=list(Line2D.markers.keys())

                format_df['Label'] = (Y_df[cla['Clase2']])#+' / '+((Y_df[cla['Clase2']]))
                
                #clases1=list(Y_df.groupby([cla["Clase1"]]).groups.keys())
                clases2=list(Y_df.groupby([cla["Clase2"]]).groups.keys())
                #dict_col=dict(zip(clases1,colores))
                dict_sim=dict(zip(clases2,simbolos))

                #y_seven = Y_df[cla['Clase1']].copy()
                y_t = Y_df[cla['Clase2']].copy()
                for i in clases2:
                    format_df.loc[y_t==i, 'Marker'] = dict_sim[i]
                format_df['Color'] = "blue"
    else: 
        format_df['Label'] = (Y_df['SubCuenca'])+' / '+((Y_df['Tipo_Pto']))
        format_df.loc[y_seven=='Rio Grande Medio', 'Color'] = 'yellow'#; format_df.loc[y_2==filtro, 'Marker'] = dtipo[filtro2]; format_df.loc[y_t==filtro2, 'Alpha']= 0.6
        format_df.loc[y_seven=='Río Guatulame', 'Color'] = 'blue'#; format_df.loc[y_2==filtro, 'Marker'] = dtipo[filtro2]; format_df.loc[y_t==filtro2, 'Alpha']= 0.6
        format_df.loc[y_seven=='Rio Limari', 'Color'] = 'lime'#; format_df.loc[y_2==filtro ,'Marker' ] = dtipo[filtro2]; format_df.loc[y_t==filtro2, 'Alpha']= 0.6
        format_df.loc[y_seven=='Rio Hurtado', 'Color'] = 'cyan'#; format_df.loc[y_2==filtro ,'Marker' ] = dtipo[filtro2]; format_df.loc[y_t==filtro2, 'Alpha']= 0.6
        format_df.loc[y_seven=='Rio Grande Bajo', 'Color'] = 'magenta'#; format_df.loc[y_2==filtro ,'Marker' ] = dtipo[filtro2]; format_df.loc[y_t==filtro2, 'Alpha']= 0.6
        format_df.loc[y_seven=='Rio Grande Alto', 'Color'] = 'red'#; format_df.loc[y_2==filtro ,'Marker' ] = dtipo[filtro2]; format_df.loc[y_t==filtro2, 'Alpha']= 0.6
        format_df.loc[y_seven=='Fuera del Area de Estudio', 'Color'] = 'white'

        
        format_df.loc[y_t=='Superficial','Marker'] = 's'
        format_df.loc[y_t=='Subterranea','Marker'] = 'o'
        format_df.loc[y_t=='Vertiente','Marker'] = 'v'
        format_df.loc[y_t=='Precipitacion','Marker'] = 'd'
        format_df.loc[y_t=='Criosfera','Marker'] = '*'
    
    
    format_df['Sample'] = format_df['Cod'].copy()
    format_df['Size'] = sz
    if std:
        format_df=escala_TDS(format_df,'TDS',sz,sz*4)
    format_df['Alpha'] = 1
    
    


    

    
    #format_df=format_df.dropna(how='any')
    format_df = format_df.sort_values(by='Label')
    

    format_df.reset_index(inplace=True, drop=True)
    #print (format_df)
    
    return format_df, lyd

def escala_TDS(df,col,s_min=25,s_max=100):
    v_min=min(df[col])
    v_max=max(df[col])
    df['Size']=s_min+(df[col]-v_min)/(v_max-v_min)*(s_max-s_min)
    df.dropna(how='any', subset='Size', inplace=True)
    #print (df['Size'])
    return df

def corregir_BD(DATA3):
    for k in DATA3.columns:
        if ',,' in k: DATA3.drop(columns=k, inplace=True)
    for k in DATA3.columns:
        if 'mg/l' in k:
            
            for i in list(DATA3.index):
                m=DATA3.at[i,k]
                if  type(m)==str:
                    try:
                        n=float(m)
                        DATA3.at[i,k]=n
                    except:
                        if '<' in m:
                            if ',' in m:
                                num=m[1:].split(',')
                                n=float(num[0]+'.'+num[1])/2
                                DATA3.at[i,k]=n
                            else:
                                num=m[1:]
                                n=float(num)/2
                                DATA3.at[i,k]=n
            cop=DATA3[k].copy()
            DATA3[k]=cop.astype('float')
            if 'arbonat' in k or 'CO3' in k:
                DATA3[k].fillna(value=0,inplace=True)
    return DATA3

def ncolorandom2(j):
    colores=list()
    clp=cm.get_cmap('tab20') if j <=20 else cm.get_cmap('gist_rainbow')
    for i in range (0,j):
        colores.append([list(clp(i/j)),])
    #n=len(colores)
    """ret=list()
    for i in range(0,j,1):
        ret.append(next(colores))"""
    #print (colores)
    return colores
def numb_sp(df,n):
    l=len(df)
    n1=float(n)
    num=int(str(l/n1+1).split('.')[0])
    x=[num,int(n)]
    lista=list()
    for i in range(1,l+1):
        x.append(i)
        lista.append(tuple(x))
        x=[num,int(n)]
    return lista

def norma(df=pd.DataFrame(),s=12,fecha='Fecha',ultimo='',primero=''):
    # Example data
    if ultimo == '': MF= max(df[fecha])
    else: MF= ultimo
    if primero == '': NF= min(df[fecha])
    else: NF= primero
    #NF=min(df[fecha])
    lst=[NF,MF]
    dff=pd.DataFrame()
    for f in lst:
        data1 = {'Cod_Muestra' : ['Nch 409', 'Nch 1333'],
                'Tipo'  : ['Nch 409', 'Nch 1333'],
                fecha:[f,f],
                'Al'     : [0.2, np.nan],
                'Cu'     : [2.0, 0.2],
                'Cr'     : [0.05, 0.1],
                'F'     : [1.5, 1.0],
                'Fe'     : [0.3, 5.0],
                'Mn'      : [0.1, 0.2],
                'Mg'   : [125.0, np.nan],
                'Se'    : [0.01, 0.02],
                'Zn'    : [3.0, 2.0],
                'As'    : [0.01, 0.1],
                'Cd'    : [0.01, 0.01],
                'Hg'    : [0.001, 0.001],
                'NO3'    : [50, np.nan],
                'Pb'    : [0.05, 5],
                'Cl'    : [400, 200],
                'SO4'    : [500, 250],
                'TDS'    : [1500, 5000],
                'pH'     : [6.5, 8.5]
                }
        dff=pd.concat([pd.DataFrame(data1),dff.copy()])
    #df2 = pd.concat([dff,df])
    
    dff.reset_index(inplace=True, drop=True)
    #print (df3['Mg'])
    # df = pd.read_csv('../data/data_template.csv')
    return dff
def plot_promedio(ax,prom,xmin,xmax,q1='',q2='',col='yellow',aph=0.3,qts=True):
    x=np.array([xmin,xmax])
    y=np.array([prom,prom])
    yq1=np.array([q1,q1])
    yq2=np.array([q2,q2])
    ax.plot(x,y,color='grey',ls='-',zorder=1)
    if qts:
        ax.plot(x,yq1,color='grey',ls=':',zorder=0)
        ax.plot(x,yq2,color='grey',ls=':',zorder=0)
        ax.fill_between(x,yq1,yq2,alpha=aph, color=col)

def grafico_2v(Bal=pd.DataFrame(), v1="rCa",v2="",xv=['pH','TDS','As','SO4','Cu','Fe','Mn','Se','Cl','Pb','Al'],
    filt=['Tipo'],fecha_filt=(True,"01-08-2022"),LOGY=True, LOGX=False, ss=12,xlim="",ylim="",f=False,inv=False,AXS=''):

    
    xlist=isinstance(xv,list)

    y_format = mticker.FuncFormatter(func)
    f_format=mticker.FuncFormatter(func_fecha)
    #print (y_format)

    dic_titulos=diccionario_titulos(xlist,v1,v2,xv)

    if not xlist:
        absi=xv
        esfecha=isinstance(Bal.at[Bal.index[0],xv],datetime.date)
        xv=[xv]
        
    else: esfecha= False
    
    listael=xv
    listaelmen=listael#['SO4','Fe','Se','Cu']
    contador=0
    if AXS=='':
        sf=plt.figure()
        sf.set_figwidth(12)
        if xlist: sf.set_figheight(4*len(listael))
        else: sf.set_figheight(12)
        
    num=numb_sp(listael,1)
    
    if fecha_filt[0]:
        ff= dt.strptime(fecha_filt[1], "%d-%m-%Y")
        P=Bal.loc[(Bal['Fecha'] >= ff)].reset_index(drop=True)
        Nch=norma(P)
        
    else: 
        P=Bal.copy()
        Nch=norma(P)
    
    if esfecha:
        P.sort_values(by='Fecha',inplace=True)
        x_min= dt.strptime(fecha_filt[1], "%d-%m-%Y")
        x_max= datetime.datetime(2022,10,1)
        Nch=norma(P,ultimo=x_max,primero=x_min)
    else: 
        #print (esfecha)
        estadis=Bal.describe()[listaelmen].T#.at['SO4','mean']
    # Eliminar val Nan
    if v2!="": drp=[v1,v2]
    else: drp=[v1]
    P.dropna(subset=xv+drp, axis=0, inplace=True)
    if isinstance(filt,list):
        try:
            dfg=P.groupby(filt)
            kg=dfg.groups.keys()
            if len(filt)>1:
                cla= {'Clase1': filt[0],
                    'Clase2': filt[1] }
                
            else: 
                cla= {'Clase1': filt[0],
                'Clase2': filt[0] }
            #dic_tmp, dic_mar = ncolran_dic(P,cla,T=(len(filt)>1))#dict(zip(list(kg),ncolorandom(len(list(kg)))))
            
            clasi=True
        except: return print (f'Error: No se puede clasificar por {filt}')
        dic_tmp, dic_mar = ncolran_dic(P,cla,T=(len(filt)>1))

            

        
        lgd_c=leyenda_2S(cla,dic_mar=dic_mar,dic_tmp=dic_tmp)
    else: 
        kg=0
        clasi=False
    
    
    for elemento in listael:
        
        

        if AXS!='': ax=AXS
        else: ax=sf.add_subplot(num[contador][0],num[contador][1],num[contador][2])
        contador+=1
        if v2 =="" and v1!="":
            div=False
        elif v1=="" and v2 =="":
            return ("Valor y inválido")
        else: div=True

        absi=elemento
        gim=0
        #dic_titulos['Ferrico']='Fe$^{+3}$'
        #print (dic_mar,dic_tmp)
        for i in list(kg):
            if i ==0: df=P
            else: df=dfg.get_group(i)
            #print (i,df[ord])
            if v2!="": drp=[v1,v2]
            else: drp=[v1]
            df.dropna(subset=xv+drp, axis=0, inplace=True)
            #print (df)
            if len(df.index)==0: continue #or df.at[df.index[0],'Tipo']=='CANDELARIA': continue
            #if df.at[df.index[0],'Tipo']=='CANDELARIA': print (df[ord])
            nombre=""
            esp=""
            for i in filt:
                if isinstance(df.at[df.index[0],i],datetime.date):
                    ad=conv_fecha(df.at[df.index[0],i])
                    
                else: ad = df.at[df.index[0],i]
                nombre+=esp+ad
                esp=" - "
            if clasi:
                #print (dic_mar)
                color=dic_tmp[df.at[df.index[0],cla['Clase1']]]
                mar=dic_mar[df.at[df.index[0],cla['Clase2']]]
            else: color, mar=('r','o')
            x=df[absi]
            ord= not div
            if div: 
                Y=df[v2]/df[v1]
                
            else:
                Y=df[v1]
               
            
            alp=1
            if i == 'Pozo':
                zord=0
                color='gray'
            else: zord = 2
            if esfecha: ax.plot(x,Y,label=nombre,ls='--',ms=ss,mfc=color,marker=mar,mec='k', alpha=alp, zorder=zord)
            elif inv: ax.scatter(Y,x,label=nombre,s=ss*4,c=color,marker=mar,edgecolors='k', alpha=alp, zorder=zord)
            else: ax.scatter(x,Y,label=nombre,s=ss*4,c=color,marker=mar,edgecolors='k', alpha=alp, zorder=zord)
            for i in listaelmen:
                    if ord and i == v1 and esfecha:
                        plot_promedio(ax=ax,prom=estadis.at[i,'mean'],xmin=x_min,xmax=x_max,q1=estadis.at[i,'75%'],
                        q2=estadis.at[i,'25%'],col='gray',aph=0.05, qts=False)
                        if gim==0:
                            if v1 in ['TDS', 'Cl', 'pH']: 
                                ubic= 'bottom'
                                ct=0.01*estadis.at[i,'mean']
                            else: 
                                ubic='top'
                                ct=-0.1*estadis.at[i,'mean']
                            plt.annotate('Promedio Cuenca Río Copiapo',(x_max,estadis.at[i,'mean']+ct),
                            fontsize=13,c='gray',rotation=0,ha='right',va=ubic)
                            gim=1
                        #print (ord ,estadis.at[i,'mean'],estadis.at[i,'75%'],estadis.at[i,'25%'])
        if AXS!='': return
        sf.tight_layout() 
        ng=Nch.groupby('Tipo')
        for ngi in list(ng.groups.keys()):
            Xg=ng.get_group(ngi)
            if not ord: continue
            if '409' in ngi: col='black'
            else: col= 'red'
            try:
                xn=Xg[x]
                yn=Xg[v1]
                if v1== 'Al': etiq='OMS'
                else: etiq=ngi
                plt.annotate(etiq,(x_max,Xg.at[Xg.index[0],ord]),fontsize=13,c=col ,rotation=0,ha='right',va='bottom')
                plt.plot(xn,yn,c=col,ls='--',zorder=1)
                
                #print(min(xn))
            except: continue
        if not inv:
            X=absi
            if ord:
                Y=v1
            else:
                P[v2+'/'+v1]=P[v2]/P[v1]
                Y=v2+'/'+v1
        else: 
            Y=absi
            if ord:
                X=v1
            else:
                P[v2+'/'+v1]=P[v2]/P[v1]
                X=v2+'/'+v1
#Definir limites de los 3 graficos

        if isinstance(xlim,tuple):# and xlim[0]!=xlim[1]:
            x_min=xlim[0]
            x_max=xlim[1]
        else:
            x_mini=min(P[X].dropna())
            x_maxi=max(P[X].dropna())
            espx=(x_maxi-x_mini)*0.1
            if LOGX:
                x_min,x_max= x_mini*0.5, x_maxi*5
            else:
                x_min=x_mini-espx
                x_max=x_maxi+espx
        if isinstance(ylim,tuple):# and ylim[0]!=ylim[1]:
            y_min=ylim[0]
            y_max=ylim[1]
        else:
            y_mini=min(P[Y].dropna())
            y_maxi=max(P[Y].dropna())
            espy=(y_maxi-y_mini)*0.1
            if LOGY:
                y_min,y_max= y_mini*0.5, y_maxi*5
            else:
                y_min=y_mini-espy
                y_max=y_maxi+espy

        if LOGY and ord!='pH':
            ax.semilogy()
            
        if LOGX:
            ax.semilogx()
            
        ax.set_ylim(y_min,y_max)
        ax.set_xlim(x_min,x_max)
        
        
            
        
        
        
        


        ## unidades f
        if absi[0]== 'r':unix=" [meq/l]"
        elif absi=='Fecha':unix=''
        else: unix=" [mg/l]"
        if v1[0]== 'r':uniy=" [meq/l]"
        elif v1[0]== '%':  uniy=""
        elif v1[0:2]== 'IS':  uniy=""
        else: uniy=" [mg/l]"

        if not inv:

            if absi=='pH': ax.set_xlabel(dic_titulos[absi])
            elif ord:
                ax.set_ylabel(dic_titulos[v1] +uniy)
                ax.set_xlabel(dic_titulos[absi]+unix)
            else: 
                ax.set_ylabel(dic_titulos[v2]+"/"+dic_titulos[v1])
                ax.set_xlabel(dic_titulos[absi]+unix)
        else:
            if absi=='pH': ax.set_ylabel(dic_titulos[absi])
            elif ord:
                
                ax.set_ylabel(dic_titulos[absi]+unix)
            else: 
                
                ax.set_ylabel(dic_titulos[absi]+unix)
            if contador == len(listael) :
                
                if ord:
                    ax.set_xlabel(dic_titulos[v1] +uniy)
                    
                else: 
                    ax.set_xlabel(dic_titulos[v2]+"/"+dic_titulos[v1])
                    
            
        if esfecha: 
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))
            plt.xticks(rotation=45)
        else:
            ax.xaxis.set_major_formatter(y_format)

        ax.get_yaxis().set_major_formatter(y_format)
        
        
        if contador == len(listael) and not f:
            lgd1=plt.legend(handles=lgd_c,bbox_to_anchor=(0.5, -0.2),borderaxespad=1,loc='upper center', markerscale=1, frameon=True, fontsize=16,
                    labelspacing=0.25,ncol=3)
            ax.add_artist(lgd1)

        

        


        #print (mm,(maxi))

        #cwd = os.getcwd()
    if not xlist and not div and not f:
        plt.savefig(f'scatter_{v1}_{xv[0]}.jpg',bbox_extra_artists=(lgd1,),bbox_inches='tight')
    elif not xlist and not f:
        plt.savefig(f'scatter_{v1}_lista.jpg',bbox_extra_artists=(lgd1,),bbox_inches='tight')
    elif xlist and not f:
        plt.savefig(f'scatter_{v1}_{v2}_lista.jpg',bbox_extra_artists=(lgd1,),bbox_inches='tight')
    else: a=1

    if not f: return 'listo'
    else: return ax, sf,lgd_c

dic_marb={'IM270 G4': 'd',
         'IM270 G12': 'h',
         'IM200': '^',
         'IM60' : 'D',
         'Pozo': 'o',
         'Río' : 's',
         'Pozo 8': 'P',
         'P12':'p',
         'HA01':'p',
         'P14':'p',
         'Vertiente': 'v',
         'Noria':'o',
         'IM135' : 'd',
         'Pozo Ag. Copayapu' : 'h',
         'Pique': '*',
         'IM256':'v',
         'IM300':'*',
         'IM170':'D',
         'IM80':'D',
         'CANDELARIA': 'P'}
         
def diccionario_titulos(xlist,v1,v2,xv):

    lista1=['Deuterio','O18','Na','Balance %','HCO3','pH','Al','TDS','Ca','Cu', 'Cr','F', 'Fe', 'Mn', 'Mg', 'Se', 'Zn','As','Cd','Hg','NO3','Pb','Cl','SO4','TDS','Ferrico']
    lista2=["$\delta^{2}$ H‰ V-SMOW","$\delta^{18}$ O‰ V-SMOW",'Na$^{+}$','Balance [%]','HCO3$^{-}$','pH','Al','Solidos Disueltos Totales','Ca$^{+2}$','Cu', 'Cr', 'F$^-$', 'Fe$_{tot}$', 'Mn','Mg$^{+2}$', 'Se', 'Zn','As','Cd','Hg','NO3$^{-2}$','Pb','Cl$^-$','SO$_4^{-2}$','TDS','Fe$^{+3}$']
    dic_titulos=dict(zip(lista1,lista2))
    if v1 not in lista1:
        if v1[1:] in lista1: dic_titulos[v1]=dic_titulos[v1[1:]]
        else:
            #print (v1[1:])
            dic_titulos[v1]= input(f"Ingrese Etiqueta para el valor {v1}")

    
    if v2 !="" and v2 not in lista1:
        if v2[1:] in lista1: dic_titulos[v2]=dic_titulos[v2[1:]]
        else: dic_titulos[v2]= input(f"Ingrese Etiqueta para el valor {v2}")

    if not xlist and xv not in lista1:
        if xv[1:] in lista1: dic_titulos[xv]=dic_titulos[xv[1:]]
        else: dic_titulos[xv]= input(f"Ingrese Etiqueta para el valor {xv}")

    elif xlist:
        for x_lab in xv:
            if  x_lab not in lista1:
                if x_lab[1:] in lista1: dic_titulos[x_lab]=dic_titulos[x_lab[1:]]
                else: dic_titulos[x_lab]=input(f"Ingrese Etiqueta para el valor {x_lab}")

    return dic_titulos

def func_fecha(ff,pos):
    a=conv_fecha(ff)
    #print (a)
    return  a


def conv_fecha(i):
    mm=str(i)[5:7]
    dd=str(i)[8:10]
    aa=str(i)[2:4]
    #print (i,mm+dd+aa)
    return (dd+'-'+mm+'-'+aa)

def grafico_bal(Bal=pd.DataFrame(), v1='Balance %',xv=['TDS'], filt=['Tipo'],fecha_filt=(True,"01-08-2022"),LOGY=True, LOGX=True, ss=12):
    
    y_format = mticker.FuncFormatter(func)
    plt.rcParams['image.cmap'] = "bwr"
    plt.rcParams['figure.dpi'] = "100"
    plt.rcParams['savefig.bbox'] = "tight"
    #style.use('default') or plt.style.use('default')
    #plt.rcParams.update({'font.size': 12})
    #plt.rcParams.update({'font.sans-serif': 'Arial'})
    if LOGY:
        Bal[v1]=abs(Bal[v1].copy())
    axs, sf,lgd_c = grafico_2v(Bal=Bal, v1=v1,xv=xv,filt=filt,fecha_filt=fecha_filt,LOGY=LOGY, LOGX=LOGX, ss=ss,f=True)
    axs.plot([0,80000],[5,5],c='black',ls=':')
    #Lineas
    sf.set_figwidth(10)
    sf.set_figheight(10)

    lim=[100,500,1000,5000,20000,50000]
    lim2=[0,100,500,1000,5000,20000,50000,80000]
    alt=50
    tit=[('Dulce',alt),(' Dulce\n moderadamente\n mineralizada',alt),
        ('Dulce\n mineralizada',alt),('Salobre',alt),('Salada',alt),('Muy salada',alt),('Salmuera',alt)]
    for i in lim:
        auy=np.asarray([i,i])
        aux=np.asarray([-0.5,50])
        plt.plot(auy,aux,c='black',ls='--')
    for i,y in tit:
        if len(i)<8:
            rota=0
        else: 
            rota=90
        c=tit.index((i,y))
        plt.annotate(i,((lim2[c]+lim2[c+1])*0.66,y), rotation=rota,ha='right',va='top')
    plt.annotate('5 %',(2.2,5), rotation=0,ha='right',va='bottom')
    axs.set_ylim(0.024,55)
    axs.set_xlim(0.2,90000)
    axs.semilogx()
    axs.semilogy()
    axs.xaxis.set_major_formatter(mticker.ScalarFormatter())
    axs.yaxis.set_major_formatter(mticker.ScalarFormatter())
    axs.get_xaxis().set_major_formatter(y_format)
    axs.get_yaxis().set_major_formatter(y_format)
    axs.set_ylabel("Error de Balance Absoluto [%]")
    axs.set_xlabel("Solidos Totales Disueltos [mg/l]")
    #axs.legend(ncol=2,fontsize=13, loc=1)
    axs.grid()
    lgd1=plt.legend(handles=lgd_c,bbox_to_anchor=(0.5, -0.15),borderaxespad=1,loc='upper center', markerscale=1, frameon=True, fontsize=16,
                    labelspacing=0.25,ncol=4)
    #axs.add_artist(lgd1)
    #print (lgd_c[0], lgd_c[1])
    #lgd1=plt.legend(lgd_c[0], lgd_c[1],bbox_to_anchor=(0.5, -0.15),borderaxespad=1,loc='upper center', markerscale=1, frameon=True, fontsize=16,
    #                labelspacing=0.25,ncol=3)
    #lgd2=plt.legend(lgd_c[2], lgd_c[3],bbox_to_anchor=(0.5, -0.15),borderaxespad=1,loc='upper center', markerscale=1, frameon=True, fontsize=16,
    #                labelspacing=0.25,ncol=3)
    #axs.add_artist(lgd1)
    #axs.add_artist(lgd2)

    sf.savefig('scatter_{}.jpg'.format('Balan_abso vs TSD_tipob' ),bbox_extra_artists=(lgd1,),bbox_inches='tight')
    return 'graf bal'


def ncolran_dic(Y_df,cla,T=True):

    
    #print (list(Line2D.filled_markers))
    simb=list(Line2D.filled_markers)
    remv=[',','None',' ']
    for r in remv:
        try:simb.remove(r)
        except: continue
    col=list(mcol.cnames.items())
    clases1=list(Y_df.groupby([cla["Clase1"]]).groups.keys())
    clases2=list(Y_df.groupby([cla["Clase2"]]).groups.keys())

    colores=ncolorandom2(len(clases1))
    simbolos=ncolorandom_ord(len(clases2),simb)
    #print (colores)            
            
    dict_col=dict(zip(clases1,colores))
    if T: dict_sim=dict(zip(clases2,simbolos))
    else:
        dict_sim=dict(zip(clases2,['o']*len(clases2)))
    return dict_col, dict_sim

def ncolorandom(j,lista=list(mcol.cnames.items())):
    val=isinstance(lista[0],tuple)
    n=len(lista)
    ret=list()
    if val:
        for i in rm.sample(range(0,n),k=j):
            ret.append(lista[i][0])
    else:
        for i in rm.sample(range(0,n),k=j):
            ret.append(lista[i])
    return ret

def ncolorandom_ord(j,lista=list(mcol.cnames.items())):
    val=isinstance(lista[0],tuple)
    n=len(lista)
    if len(lista)<j:
        listafin=lista*(int(j/len(lista))+1)
    else: listafin=lista
    ret=list()
    if val:
        for i in rm.sample(range(0,n),k=j):
            ret.append(lista[i][0])
    else:
        ret=listafin[0:(j)]
        
    return ret

    ########### Funcion de ISOTOPOS #########################
#########################################################

def graf_isotopos(ax,rectas_aux=dict(),xlim=(-15,0),ylim=(-110,0),zoom=True,z_dom=(-11,-9.3,-88,-73),z_ubi=(-14,-40),z_dim=(6,40),dic_gp=dict()):
    if rectas_aux == dict():
        rectas_aux={'Línea de evaporación': (5.454,-23.89,':','\n(Troncoso et. al., 2012)'),
                    'Línea Meteórica Local': (8.07,+13.5,'--','\n(Troncoso et. al., 2012)'),
                    'Línea Meteórica Mundial': (8,10,'-','(Craig, 1961)')}
        return rectas_aux
    if dic_gp == dict():
        return ('Error, Ingrese variables del grafico en forma de diccionario')
    axl=[ax]
    aux=np.asarray([0.01,1000])
    a=rectas_aux['Línea de evaporación'][0]
    b=rectas_aux['Línea de evaporación'][1]
    aux[0]=(b-rectas_aux['Línea Meteórica Local'][1])/(+rectas_aux['Línea Meteórica Local'][0]-a)
    dxlim=xlim[1]-xlim[0]
    xl=aux[0]
    xf=xl+dxlim

    

    if zoom:
        yl, yf = xl*abs(ylim[0])/dxlim, xf*abs(ylim[0])/dxlim
        

        x1,x2,y1,y2 =z_dom[0],z_dom[1],z_dom[2],z_dom[3]


        axin_x, axin_y = z_ubi
        largo, alto = z_dim
        
        axins=ax.inset_axes([1-(xf-(axin_x))/(xf-xl),1-(yf-(axin_y))/(yf-yl),largo/(xf-xl),alto/(yf-yl)]) #[1-abs(axin_x)/(xf-xl),1-abs(axin_y)/(yf-yl),0.47,0.47]
        
        
        
        axl.append(axins)
    ax.set_xlim(xl,xf)
    ax.set_ylim(yl,yf)
    aux=np.asarray([-20,12.5])

    for axs in axl:
        for ky in rectas_aux.keys():
            axs.plot(aux[0:2],aux[0:2]*rectas_aux[ky][0]+rectas_aux[ky][1],c='black',ls=rectas_aux[ky][2],label=ky+rectas_aux[ky][3])
    
    if zoom:
        axins.set_xlim(x1, x2)
        axins.set_ylim(y1, y2)
        axins.set_xticklabels([])
        axins.set_yticklabels([])
        ax.indicate_inset_zoom(axins, edgecolor="black",lw=2)

    DCG= dic_gp
    DCGK=list(DCG.keys())

    grafico_2v(Bal=DCG[DCGK[0]],v1=DCG[DCGK[1]],v2=DCG[DCGK[2]],xv=DCG[DCGK[3]],filt=DCG[DCGK[4]],LOGY=DCG[DCGK[5]],LOGX=DCG[DCGK[6]],f=DCG[DCGK[7]],ss=DCG[DCGK[8]], inv=DCG[DCGK[9]],xlim=DCG[DCGK[10]],AXS=axins)
    return axins
################################# FIN FUNC ISOTOPOS ##################################################3
### funcion leyenda###
def leyenda_2S(cla,dic_mar,dic_tmp):
    lgdM=list()
    lgdC=list()
    if cla['Clase1']==cla['Clase2']:
            for dc in dic_mar.keys():
                if isinstance(dc,datetime.date): ndc= conv_fecha(dc)
                else: ndc=dc
                
                lgdM.append(mlines.Line2D([],[],markerfacecolor=dic_tmp[dc][0],markeredgecolor='k',marker=dic_mar[dc],linestyle='None', markersize=8, label=ndc))
    else:
        for dc in dic_mar.keys():
            if isinstance(dc,datetime.date): ndc= conv_fecha(dc)
            else: ndc=dc
            lgdM.append(mlines.Line2D([],[],markerfacecolor='none',markeredgecolor='k',marker=dic_mar[dc],linestyle='None', markersize=8, label=ndc))
        for dc in dic_tmp.keys():
            if isinstance(dc,datetime.date): ndc= conv_fecha(dc)
            else: ndc=dc
            lgdC.append(mlines.Line2D([],[],color=dic_tmp[dc][0],marker='o',markeredgecolor='k',linestyle='None', markersize=10, label=ndc))
    lgd_c=lgdM+lgdC
    return lgd_c