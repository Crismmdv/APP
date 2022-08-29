# -*- coding: utf-8 -*-
import pandas as pd
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
    
    si=int(s)
    if x-si!=0:
        coma, dc=(',','%s'% (x-si))
    else:
        coma, dc= ('','')
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    if xx<0: return '-'+s + '.'.join(reversed(groups))+coma+dc[2:]   
    else: return s + '.'.join(reversed(groups))+coma+dc[2:]

def creardf_sc(Y_df,filtro='',filtro2='',sz=8):
    format_df = pd.DataFrame()
    #filtro='F.A.E'
    #filtro2=''
    #sz=8
    Y_df['TDS']=Y_df['STD_mg_l'].copy()
    y_seven = Y_df['SubCuenca'].copy() 
    y_2 = Y_df['Contexto_H'].copy()
    y_t = Y_df['Tipo_Pto'].copy()
    y_tds = Y_df['TDS'].copy()

    if filtro != '':
        Z_df=Y_df.groupby('SubCuenca').get_group(filtro)
    else:
        Z_df=Y_df
    dtipo=dict({'subterránea':'o','superficial':'s','vertiente':'v', 'precipitación':'d','criósfera':'*'})

    if filtro2 != '':
        format_df['Marker'] = dtipo[filtro2]
        M_df=Z_df.groupby('Tipo_Pto').get_group(filtro2)
        format_df['Label'] = (M_df['Contexto_H']).map(str)#+' - '+(M_df['SCIc']).map(str)
    else:
        M_df=Z_df.copy()
        format_df['Label'] = (M_df['Contexto_H']).map(str)+' / '+(M_df['Tipo_Pto']).map(str)
    


    format_df['Sample'] = M_df['Cod_Muestr']
    #format_df['Label'] = (M_df['SCI']).map(str)#+'- '+(M_df['SCIb']).map(str)

    #format_df = format_df.sort_values(by='Label')

    format_df.loc[y_2=='A1', 'Color'] = 'red'#; format_df.loc[y_2==filtro, 'Marker'] = dtipo[filtro2]; format_df.loc[y_t==filtro2, 'Alpha']= 0.6
    format_df.loc[y_2=='A2', 'Color'] = 'darkorange'#; format_df.loc[y_2==filtro, 'Marker'] = dtipo[filtro2]; format_df.loc[y_t==filtro2, 'Alpha']= 0.6
    format_df.loc[y_2=='A3', 'Color'] = 'lime'#; format_df.loc[y_2==filtro ,'Marker' ] = dtipo[filtro2]; format_df.loc[y_t==filtro2, 'Alpha']= 0.6
    format_df.loc[y_2=='B1', 'Color'] = 'darkviolet'#; format_df.loc[y_2==filtro ,'Marker' ] = dtipo[filtro2]; format_df.loc[y_t==filtro2, 'Alpha']= 0.6
    format_df.loc[y_2=='B2', 'Color'] = 'blue'#; format_df.loc[y_2==filtro ,'Marker' ] = dtipo[filtro2]; format_df.loc[y_t==filtro2, 'Alpha']= 0.6
    format_df.loc[y_2=='B4', 'Color'] = 'cyan'#; format_df.loc[y_2==filtro ,'Marker' ] = dtipo[filtro2]; format_df.loc[y_t==filtro2, 'Alpha']= 0.6
    format_df.loc[y_2=='C1', 'Color'] = 'pink'
    format_df.loc[y_2=='D1', 'Color'] = 'gold'
    format_df.loc[y_2=='D2', 'Color'] = 'gray'
    format_df.loc[y_2=='D3', 'Color'] = 'black'
    format_df.loc[y_2=='F.A.E', 'Color'] = 'white'
    #['red','darkorange','lime','darkviolet','blue','cyan','pink','gold','gray','black','white']

    if filtro2=='':
        format_df.loc[y_t=='superficial','Marker'] = 's'
        format_df.loc[y_t=='subterránea','Marker'] = 'o'
        format_df.loc[y_t=='vertiente','Marker'] = 'v'
        format_df.loc[y_t=='precipitación','Marker'] = 'd'
        format_df.loc[y_t=='criósfera','Marker'] = 'D'
        format_df.loc[y_t=='superficial','Size'] = sz
        format_df.loc[y_t=='subterránea','Size'] = sz
        format_df.loc[y_t=='vertiente','Size'] = sz
        format_df.loc[y_t=='precipitación','Size'] = sz
        format_df.loc[y_t=='criósfera','Size'] = sz
    #format_df.loc[y_t==filtro2, 'Alpha']= 0.6
    #format_df.loc[y_seven=='A2', 'Color'] = 'orange'; format_df.loc[y_2=='Precipitación', 'Marker'] = 'd'
    else: 
        format_df.loc[y_t==filtro2,'Marker'] = dtipo[filtro2]
        format_df.loc[y_t==filtro2,'Size'] = sz
    #format_df['Marker'] = dtipo[filtro2]
    #format_df['Size'] = 25
    format_df['Alpha'] = 1
    if filtro2=='criósfera':
        format_df['Size'] = sz

    format_df['Cu'] = M_df['Cu_mg_l']
    format_df['Cr'] = M_df['Cr_mg_l']
    format_df['F'] = M_df['F_mg_l']
    format_df['Fe'] = M_df['Fe_mg_l']              
    format_df['Mn'] = M_df['Mn_mg_l']   
    format_df['Mg'] = M_df['Mg_mg_l']
    format_df['Se'] = M_df['Se_mg_l']
    format_df['Zn'] = M_df['Zn_mg_l']
    format_df['As'] = M_df['As_mg_l']
    format_df['Cd'] = M_df['Cd_mg_l']
    format_df['Hg'] = M_df['Hg_mg_l']
    format_df['NO3'] = M_df['NO3_mg_l']
    format_df['Pb'] = M_df['Pb_mg_l']
    format_df['Cl'] = M_df['Cl_mg_l']
    format_df['SO4'] = M_df['SO4_mg_l']
    format_df['TDS']= M_df['TDS']*1.000

    format_df=format_df.dropna(how='any')
    format_df = format_df.sort_values(by='Label')
    # Reset the index
    #format_df['SO4'] = pd.to_numeric(format_df['SO4'], errors='coerce')

    format_df.reset_index(inplace=True, drop=True)

    #format_df.to_csv(r'C:/Users/crist/Desktop/Sernageomin/GIS LIMARI/QGIS/HICT_Rio_Grande.csv', index=False)
    # Show the df
    a=filtro
    b=filtro2
    return format_df#,a,b

def creardf_piper(Y_df,filtro='',filtro2='',sz=25, di=dict(),cla=""):
    format_df = pd.DataFrame()
    #filtro='F.A.E'
    #filtro2=''
    diccion=di
    for i in diccion.keys():
        
        format_df[i]=Y_df[diccion[i]].copy()
    
    if False:
        return (Y_df)
    #if filtro!='' and filtro2 == '':
    #    format_df=format_sf.groupby([filtro])
    #    return (format_df)
    #elif filtro !='' and filtro2 !='':
    #    format_df=format_sf.groupby([filtro,filtro2])
    #    return (format_df)
    else:
        #y_tds=Y_df['STD_mg_l'].copy()
        #y_seven = Y_df['SubCuenca'].copy() 
        #y_2 = Y_df['Contexto_H'].copy()
        #y_t = Y_df['Tipo_Pto'].copy()
        
        
        #format_df=format_sf.copy()
        if cla=="":
            format_df['Label'] = "Muestras"
            format_df['Color'] = "gray"
            format_df['Marker'] = "o"
        elif len(cla)==2:
            
            colores=['red','darkorange','lime','darkviolet','blue','cyan','pink','olive','mediumpurple','blueviolet',
                'gold','gray','black','white','green','gray','magenta','skyblue', 'indigo','purple','brown','indigo','darkcyan']
            simbolos =["*","d","o","s","v"]

            format_df['Label'] = (Y_df[cla['Clase1']])+' / '+((Y_df[cla['Clase2']]))
            
            clases1=list(Y_df.groupby([cla["Clase1"]]).groups.keys())
            clases2=list(Y_df.groupby([cla["Clase2"]]).groups.keys())
            dict_col=dict(zip(clases1,colores))
            dict_sim=dict(zip(clases2,simbolos))

            y_seven = Y_df[cla['Clase1']].copy()
            y_t = Y_df[cla['Clase2']].copy()

            for i in clases1:
                format_df.loc[y_seven==i, 'Color'] = dict_col[i]
            for i in clases2:
                format_df.loc[y_t==i, 'Marker'] = dict_sim[i]
            
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
                    #colores=['red','darkorange','lime','darkviolet','blue','cyan','pink','olive','mediumpurple','blueviolet',
                    #   'gold','gray','black','white','green','gray','magenta','skyblue', 'indigo','purple','brown','indigo','darkcyan']
                    simbolos =["*","d","o","s","v"]

                    format_df['Label'] = (Y_df[cla['Clase2']])#+' / '+((Y_df[cla['Clase2']]))
                    
                    #clases1=list(Y_df.groupby([cla["Clase1"]]).groups.keys())
                    clases2=list(Y_df.groupby([cla["Clase2"]]).groups.keys())
                    #dict_col=dict(zip(clases1,colores))
                    dict_sim=dict(zip(clases2,simbolos))

                    #y_seven = Y_df[cla['Clase1']].copy()
                    y_t = Y_df[cla['Clase2']].copy()
                    for i in clases2:
                        format_df.loc[y_t==i, 'Marker'] = dict_sim[i]
                    format_df['Color'] = "grey"
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
        format_df['Alpha'] = 1
        
        


        

        
        format_df=format_df.dropna(how='any')
        format_df = format_df.sort_values(by='Label')
        

        format_df.reset_index(inplace=True, drop=True)
        #print (format_df)
        
        return format_df