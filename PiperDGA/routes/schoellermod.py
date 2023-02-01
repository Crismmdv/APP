# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 13:11:29 2021

@author: Jing
"""
from dataclasses import replace
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as mticker

from .ions import ions_WEIGHT, ions_CHARGE

# Define the plotting function
def func(x, pos):  # formatter function takes tick label and tick position
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
    return s + '.'.join(reversed(groups))+coma+dc[2:]

def mod_df(df1,df2,nch):
    d1333=dict(zip(['Al','Cu', 'Cr','F', 'Fe', 'Mn','Se', 'Zn','As','Cd','Hg','Pb','Cl','SO4','TDS'],['Al','Cu', 'Cr', 'F$^-$', 'Fe$_{tot}$', 'Mn', 'Se', 'Zn','As','Cd','Hg','Pb','Cl$^-$','SO$_4^{2-}$','TDS']))
    d409=dict(zip(['Al','Cu', 'Cr','F', 'Fe', 'Mn', 'Mg', 'Se', 'Zn','As','Cd','Hg','NO3','Pb','Cl','SO4','TDS'],['Al','Cu', 'Cr', 'F$^-$', 'Fe$_{tot}$', 'Mn', 'Mg$^{2+}$', 'Se', 'Zn','As','Cd','Hg','NO$_{3}$','Pb','Cl$^-$','SO$_4^{2-}$','TDS']))
    res = [x for x in df1 + df2 if x not in df1]
    df2.drop(res, axis=1 , inplace=True)
    Lticks409=list()
    #Lticks1333=list()
    if nch =="Nch 409": ticks=[x for x in list(d409.keys()) if (x in list(df2.columns))]# and x in list(d409.keys()))]
    else: ticks=[x for x in list(d1333.keys()) if (x in list(df2.columns))]# and x in list(d409.keys()))]
    #ticks1333=list(df2.columns)
    for i in ticks:
        try: Lticks409.append(d409[i])
        except: continue
    nticks=list(range(1,len(Lticks409)+1))
    return ticks, Lticks409, nticks
def norma(df,s,t,v):
    # Example data
    data = {'Sample' : ['Nch 409', 'Nch 1333'],
            'Label'  : ['Nch 409', 'Nch 1333'],
            'Color'  : ['k', 'r'],
            'Marker' : ['o', 'o'],
            'Size'   : [s, s],
            'Alpha'  : [1, 1],
            'Cu'     : [2.0, 0.2],
            'Al'     : [0.2, np.nan],
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
            }
    df2 = pd.DataFrame(data)
    #print (df.columns)
    if True: #not t: MODIFICADO PARA 2 
        df3= pd.concat([df,df2])
    else:
        df3= pd.concat([df,df2[(df2['Label']==v)]])
        
    df3.reset_index(inplace=True, drop=True)
    #print (df3.columns)
    # df = pd.read_csv('../data/data_template.csv')
    return (df3,df2)

def plot_scholler(dft, 
         unit='mg/L', 
         figname='Diagrama Schoeller ', 
         figformat='jpg',ms=4,n=False, nch='Nch 409',fg='',lyd=list() ):
    n2=n or (not n and nch=='Nch 1333')
    df,norm= norma(dft,1,n2,nch)
    dflb,normlb= norma(dft,1,False,nch)#para la leyenda doble
    dic={'Nch 409':0,'Nch 1333':1}
    if n or (not n and nch=='Nch 1333'):
        for i in df.columns:
            if df[i].dtypes != 'object' and i!='Size':
                df[i]=df[i]/(norm[i][dic[nch]])
    
    #print (df)
    """Plot the HFE-D  diagram.
    
    Parameters
    ----------
    df : class:`pandas.DataFrame`
        Geochemical data to draw HFE-D diagram.
    unit : class:`string`
        The unit used in df. Currently only mg/L is supported. 
    figname : class:`string`
        A path or file name when saving the figure.
    figformat : class:`string`
        The file format, e.g. 'png', 'pdf', 'svg'
        
        
    References
    ----------
    .. [1] Güler, et al. 2002.
           Evaluation of graphical and multivariate statistical methods for classification of water chemistry data
           Hydrogeology Journal 10(4):455-474
           https://doi.org/10.1007/s10040-002-0196-6
    """
    #plt.style.use('default')
    plt.style.use('ggplot') or plt.style.use('ggplot')
    plt.rcParams['font.size'] = 18
    plt.rcParams['axes.labelsize'] = 18
    plt.rcParams['axes.labelweight'] = 'normal'
    plt.rcParams['axes.titlesize'] = 18
    plt.rcParams['xtick.labelsize'] = 18
    plt.rcParams['ytick.labelsize'] = 18
    plt.rcParams['legend.fontsize'] = 18
    plt.rcParams['figure.titlesize'] = 18   
    plt.rcParams['font.family']='sans-serif'
    plt.rcParams['font.sans-serif']=['Arial']
    plt.rcParams["mathtext.fontset"]='dejavusans'
    # Determine if the required geochemical parameters are defined. 
    if not {'Cu', 'Cr','F', 'Fe', 'Mn', 'Mg', 'Se', 'Zn','As','Cd','Hg','NO3','Pb','Cl','SO4','TDS'}.issubset(df.columns):
        raise RuntimeError("""
        Schoeller diagram uses geochemical parameters not provided.
        Confirm that these parameters are provided in the input file.""")
        
    # Determine if the provided unit is allowed
    ALLOWED_UNITS = ['mg/L', 'meq/L']
    if unit not in ALLOWED_UNITS:
        raise RuntimeError("""
        Currently only mg/L and meq/L are supported.
        Convert the unit manually if needed.""")
    #se crean listas con arreglo reeducido
    ticks, Lticks, nticks =mod_df(dft,df,nch)
    # Convert unit if needed
    # -------------------------------------------------------------------------
    if unit != 'mg/L':#mod
        gmol = np.array([ions_WEIGHT['Ca'], 
                         ions_WEIGHT['Mg'], 
                         ions_WEIGHT['Na'], 
                         ions_WEIGHT['K'], 
                         ions_WEIGHT['Cl'], 
                         ions_WEIGHT['SO4'],
                         ions_WEIGHT['HCO3']])
    
        eqmol = np.array([ions_CHARGE['Ca'], 
                          ions_CHARGE['Mg'], 
                          ions_CHARGE['Na'], 
                          ions_CHARGE['K'],
                          ions_CHARGE['Cl'],
                          ions_CHARGE['SO4'],
                          ions_CHARGE['HCO3']])
    
        tmpdf = df[['Cu', 'Cr', 'Fe', 'Mn', 'Mg', 'Se', 'Zn','As','Cd','Hg','NO3','Pb','Cl','SO4','TDS']]
        dat = tmpdf.values
        
        meqL = (dat / abs(gmol)) * abs(eqmol)
        
    elif nch=='Nch 1333':
        #meqL = df[['Cu', 'Cr','F', 'Fe', 'Mn','Se', 'Zn','As','Cd','Hg','Pb','Cl','SO4','TDS']].values #mod
        meqL = df[ticks].values
    elif nch=='Nch 409':
        #meqL = df[['Cu', 'Cr','F', 'Fe', 'Mn', 'Mg', 'Se', 'Zn','As','Cd','Hg','NO3','Pb','Cl','SO4','TDS']].values
        meqL = df[ticks].values
    else:
        #meqL = df[['Cu', 'Cr','F', 'Fe', 'Mn', 'Mg', 'Se', 'Zn','As','Cd','Hg','NO3','Pb','Cl','SO4','TDS']].values
        meqL = df[ticks].values
        raise RuntimeError("""
        Currently only mg/L and meq/L are supported.
        Convert the unit if needed.""")
        
    # Do the plot
    # -------------------------------------------------------------------------
    if not n and nch=='Nch 409' and fg =='':
        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(111)
    else:
        if fg=='':
            fig = plt.figure(figsize=(15, 10))
        else:
            fig=fg
        if fg!='':
            ax = fig.add_subplot(212)
        else:
            ax = fig.add_subplot(211)
    ax.semilogy()
    
    # Plot the lines
    # -------------------------------------------------------------------------
    Labels = []
    if not n and nch=='Nch 1333':
        Labels.append(dflb.at[len(dflb)-1, 'Label'])
        ak=0
    df['Size']= ms

    for i in range(len(df)):
        if (df.at[i, 'Label'] in Labels or df.at[i, 'Label'] == ''):
            TmpLabel = ''
        else:
            TmpLabel = dflb.at[i, 'Label']
            Labels.append(TmpLabel)
    
        try:
            marker=df.at[i, 'Marker']
            color=df.at[i, 'Color']
            if df.at[i, 'Label']=='Nch 409' or df.at[i, 'Label']=='Nch 1333':
                line='-'
                marker=''
            else:
                line=':'
                #fmt=marker+color
            #print (fmt)
            if not n and nch=='Nch 1333':
                #ax.plot([1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 11, 12, 13, 14], meqL[i, :],
                ax.plot(nticks, meqL[i, :], 
                        alpha=df.at[i, 'Alpha'],
                        label=TmpLabel,
                        mec='k',
                        ls=line,
                        ms=df.at[i, 'Size'],
                        c=color,
                        marker=marker)
            else:
                #ax.plot([1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 11, 12, 13, 14, 15, 16], meqL[i, :],
                ax.plot(nticks, meqL[i, :],
                        marker=marker, 
                        c=color,
                        ls=line,
                        alpha=df.at[i, 'Alpha'],
                        label=TmpLabel,
                        mec='k',
                        ms=df.at[i, 'Size'])
            #ax.plot([1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 11, 12, 13, 14, 15, 16], meqL[i, :], 
            #        marker=df.at[i, 'Marker'],
            #        color=df.at[i, 'Color'], 
            #        alpha=df.at[i, 'Alpha'],
            #        label=TmpLabel,mec='black',
            #        ms=df.at[i, 'Size'])
        except(ValueError):
                pass
    y_format = mticker.FuncFormatter(func)  # make formatter        
    # Background settings
    if not n and nch=='Nch 1333':
        #ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 11, 12, 13, 14])
        ax.set_xticks(nticks)
        #ax.set_xticklabels(['Cu', 'Cr', 'F$^-$', 'Fe$_{tot}$', 'Mn', 'Se', 'Zn','As','Cd','Hg','Pb','Cl$^-$','SO$_4^{2-}$','TDS'])
        ax.set_xticklabels(Lticks)
        ax.set_yticks([0.001,0.01,0.1,1,10,50,1000,10000],minor=False)
    else:
        #ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 11, 12, 13, 14, 15, 16])
        #ax.set_xticklabels(['Cu', 'Cr', 'F$^-$', 'Fe$_{tot}$', 'Mn', 'Mg$^{2+}$', 'Se', 'Zn','As','Cd','Hg','NO$_{3}$','Pb','Cl$^-$','SO$_4^{2-}$','TDS'])
        ax.set_xticks(nticks)
        ax.set_xticklabels(Lticks)
        ax.set_yticks([0.0001,0.001,0.01,0.1,1,10,100,1000,10000],minor=False)
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.get_yaxis().set_major_formatter(y_format)
    if n: 
        ax.set_title(figname)
        ax.title.set_size(22)

    if n: ylab='Normalizado [Nch 409]'
    else: ylab='Concentración [mg/l]' 
    ax.set_ylabel(ylab, fontsize=18, weight='normal')#mod
    
    # Set the limits
    #ax.set_xlim([1, 16])
    #print (np.min(meqL), np.max(meqL))
    #if n:
    ax.set_ylim([0.00001, 10000])
    #else:
    #    ax.set_ylim([0.0001, 1000])
    # Plot the vertical lines
    if (n and nch=='Nch 1333') or (not n and nch=='Nch 1333'):
        for xtick in nticks:
            plt.axvline(xtick, linewidth=1.5, color='grey', linestyle='dashed')
    else:
        for xtick in nticks:
            plt.axvline(xtick, linewidth=1.5, color='grey', linestyle='dashed')
            
    # Creat the legend
    if not n:
        #print (lyd==list())
        # lgd= ax.legend(bbox_to_anchor=(0.5, -0.1),borderaxespad=1,loc='upper center', markerscale=1, frameon=True, fontsize=16,
        #           labelspacing=0.25,ncol=4,edgecolor='black',framealpha=0.3)
        if lyd==list():
            lgd=plt.legend(bbox_to_anchor=(0.5, -0.1), markerscale=1, fontsize=16, borderaxespad=1,
                    frameon=True, loc="upper center",
                    labelspacing=0.25, handletextpad=0.25,ncol=4,edgecolor='black',framealpha=0.3)
        else:
            lgd=plt.legend(handles=lyd,bbox_to_anchor=(0.5, -0.1), markerscale=1, fontsize=16, borderaxespad=1,
                    frameon=True, loc="upper center",
                    labelspacing=0.25, handletextpad=0.25,ncol=4,edgecolor='black',framealpha=0.3)
    # Display the info
    cwd = os.getcwd()
    #print("Schoeller diagram created. Saving it to %s \n" %cwd)
    fig.tight_layout()
    # Save the figure
   
    
    
    if n:
        #fig.savefig(figname + '.' + figformat, format=figformat, dpi=300)
        return plot_scholler(dft, unit='mg/L', figname='Diagrama Schoeller ', figformat='jpg',ms=ms,n=False, nch='Nch 409',fg=fig,lyd=lyd)
    else:
        #fig.savefig(figname + '.' + figformat,bbox_extra_artists=(lgd,), bbox_inches='tight', format=figformat, dpi=300)
        return fig
    
    
