# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 14:34:07 2021

@author: Jing
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from .ions import ions_WEIGHT, ions_CHARGE

# Define the plotting function
def plotpiper(df, 
         unit='mg/L', 
         figname='triangle Piper diagram', 
         figformat='jpg',nc=1):
    """Plot the Piper diagram.
    
    Parameters
    ----------
    df : class:`pandas.DataFrame`
        Geochemical data to draw Gibbs diagram.
    unit : class:`string`
        The unit used in df. Currently only mg/L and meq/L are supported. 
    figname : class:`string`
        A path or file name when saving the figure.
    figformat : class:`string`
        The figure format to be saved, e.g. 'png', 'pdf', 'svg'
        
        
    References
    ----------
    .. [1] Piper, A.M. 1944.
           A Graphic Procedure in the Geochemical Interpretation of 
           Water-Analyses. Eos, Transactions American Geophysical 
           Union, 25, 914-928.
           http://dx.doi.org/10.1029/TR025i006p00914
    .. [2] Hill, R.A. 1944. 
           Discussion of a graphic procedure in the geochemical interpretation 
           of water analyses. EOS, Transactions American Geophysical 
           Union 25, no. 6: 914–928.    
    """
    # Basic data check 
    # -------------------------------------------------------------------------
    # Determine if the required geochemical parameters are defined. 
    if not {'Ca', 'Mg', 'Na', 'K', 
            'HCO3', 'CO3', 'Cl', 'SO4'}.issubset(df.columns):
        raise RuntimeError("""
        Trilinear Piper diagram requires geochemical parameters:
        Ca, Mg, Na, K, HCO3, CO3, Cl, and SO4.
        Confirm that these parameters are provided in the input file.""")
        
    # Determine if the provided unit is allowed
    ALLOWED_UNITS = ['mg/L', 'meq/L']
    if unit not in ALLOWED_UNITS:
        raise RuntimeError("""
        Currently only mg/L and meq/L are supported.
        Convert the unit manually if needed.""")
        
    # Global plot settings
    # -------------------------------------------------------------------------
    # Change default settings for figures
    plt.style.use('default')
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.labelweight'] = 'normal'
    plt.rcParams['axes.titlesize'] = 10
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 10   
    plt.rcParams['font.family']='sans-serif'
    plt.rcParams['font.sans-serif']=['Arial']
    plt.rcParams["mathtext.fontset"]='dejavusans'
    
    
    # Plot background settings
    # -------------------------------------------------------------------------
    # Define the offset between the diamond and traingle
    offset = 0.10                         
    offsety = offset * np.tan(np.pi / 3.0)
    h = 0.5 * np.tan(np.pi / 3.0)
    
    # Calculate the traingles' location 
    ltriangle_x = np.array([0, 0.5, 1, 0])
    ltriangle_y = np.array([0, h, 0, 0])
    rtriangle_x = ltriangle_x + 2 * offset + 1
    rtriangle_y = ltriangle_y
    
    # Calculate the diamond's location 
    diamond_x = np.array([0.5, 1, 1.5, 1, 0.5]) + offset
    diamond_y = h * (np.array([1, 2, 1, 0, 1])) + (offset * np.tan(np.pi / 3))
    
    # Plot the traingles and diamond
    fig = plt.figure(figsize=(10, 10), dpi=100)
    ax = fig.add_subplot(111, aspect='equal', frameon=False, 
                         xticks=[], yticks=[])
    ax.plot(ltriangle_x, ltriangle_y, '-k', lw=1.0)
    ax.plot(rtriangle_x, rtriangle_y, '-k', lw=1.0)
    ax.plot(diamond_x, diamond_y, '-k', lw=1.0)
    
    # Plot the lines with interval of 20%
    interval = 0.5
    ticklabels = ['0','50','100']
    for i, x in enumerate(np.linspace(0, 1, int(1/interval+1))):
        # the left traingle
        ax.plot([x, x - x / 2.0], 
                [0, x / 2.0 * np.tan(np.pi / 3)], 
                'k-', lw=1.0)
        ## the bottom ticks
        if i in [1]: 
            ax.text(x, 0-0.03, ticklabels[-i-1], 
                    ha='center', va='center')
        ax.plot([x, (1-x)/2.0+x], 
                 [0, (1-x)/2.0*np.tan(np.pi/3)], 
                 'k-', lw=1.0)
        ## the right ticks
        if i in [1]:
            ax.text((1-x)/2.0+x + 0.026, (1-x)/2.0*np.tan(np.pi/3) + 0.015, 
                    ticklabels[i], ha='center', va='center', rotation=0)
        ax.plot([x/2, 1-x/2], 
                [x/2*np.tan(np.pi/3), x/2*np.tan(np.pi/3)], 
                'k-', lw=1.0)
        ## the left ticks
        if i in [1]:
            ax.text(x/2 - 0.026, x/2*np.tan(np.pi/3) + 0.015, 
                    ticklabels[i], ha='center', va='center', rotation=0)
        
        # the right traingle
        ax.plot([x+1+2*offset, x-x/2.0+1+2*offset], 
                [0, x/2.0*np.tan(np.pi/3)], 
                'k-', lw=1.0)
        ## the bottom ticks
        if i in [1]:
            ax.text(x+1+2*offset, 0-0.03, 
                    ticklabels[i], ha='center', va='center')
        ax.plot([x+1+2*offset, (1-x)/2.0+x+1+2*offset],
                 [0, (1-x)/2.0*np.tan(np.pi/3)], 
                 'k-', lw=1.0)
        ## the right ticks
        if i in [1]:
            ax.text((1-x)/2.0+x+1+2*offset  + 0.026, (1-x)/2.0*np.tan(np.pi/3) + 0.015, 
                    ticklabels[-i-1], ha='center', va='center', rotation=0)
        ax.plot([x/2+1+2*offset, 1-x/2+1+2*offset], 
                [x/2*np.tan(np.pi/3), x/2*np.tan(np.pi/3)], 
                'k-', lw=1.0)
        ## the left ticks
        if i in [1]:
            ax.text(x/2+1+2*offset - 0.026, x/2*np.tan(np.pi/3) + 0.015, 
                    ticklabels[-i-1], ha='center', va='center', rotation=0)
        
        # the diamond
        ax.plot([0.5+offset+0.5/(1/interval)*x/interval, 1+offset+0.5/(1/interval)*x/interval], 
                 [h+offset*np.tan(np.pi/3)+0.5/(1/interval)*x/interval*np.tan(np.pi/3), offset*np.tan(np.pi/3)+0.5/(1/interval)*x/interval*np.tan(np.pi/3)], 
                 'k-', lw=1.0)
        ## the upper left and lower right
        if i in [1]: 
            ax.text(0.5+offset+0.5/(1/interval)*x/interval  - 0.026, h+offset*np.tan(np.pi/3)+0.5/(1/interval)*x/interval*np.tan(np.pi/3) + 0.015, ticklabels[i], 
                    ha='center', va='center', rotation=0)
            #ax.text(1+offset+0.5/(1/interval)*x/interval + 0.026, offset*np.tan(np.pi/3)+0.5/(1/interval)*x/interval*np.tan(np.pi/3) - 0.015, ticklabels[-i-1], 
            #        ha='center', va='center', rotation=0)
        ax.plot([0.5+offset+0.5/(1/interval)*x/interval, 1+offset+0.5/(1/interval)*x/interval], 
                 [h+offset*np.tan(np.pi/3)-0.5/(1/interval)*x/interval*np.tan(np.pi/3), 2*h+offset*np.tan(np.pi/3)-0.5/(1/interval)*x/interval*np.tan(np.pi/3)], 
                 'k-', lw=1.0)
        ## the lower left and upper right
        if i in [1]:  
            #ax.text(0.5+offset+0.5/(1/interval)*x/interval- 0.026, h+offset*np.tan(np.pi/3)-0.5/(1/interval)*x/interval*np.tan(np.pi/3) - 0.015, ticklabels[i], 
            #        ha='center', va='center', rotation=0)
            ax.text(1+offset+0.5/(1/interval)*x/interval + 0.026, 2*h+offset*np.tan(np.pi/3)-0.5/(1/interval)*x/interval*np.tan(np.pi/3) + 0.015, ticklabels[-i-1], 
                    ha='center', va='center', rotation=0)
    
    # Labels and title
    plt.text(0, -offset*0.5, r"$\mathsf{Ca^{2+}}$", 
             ha='center', va='center', fontsize=10)
    plt.text(1+2*offset+1, -offset*0.5, r"$\mathsf{Cl^{-}}$", 
            ha='center', va='center', fontsize=10)
    plt.text(0.5, 0.5*np.tan(np.pi/3)+offset*0.5, r"$\mathsf{Mg^{2+}}$",  
             ha='center', va='center', rotation=0, fontsize=10)
    plt.text(1.5+2*offset, 0.5*np.tan(np.pi/3)+offset*0.5, r"$\mathsf{SO_4^{2-}}$",  
              ha='center', va='center', rotation=0, fontsize=10)
    plt.text(1, -offset*0.5, r"$\mathsf{Na^{+} + K^{+}}$",  
              ha='right', va='center', rotation=0, fontsize=10)
    plt.text(1+2*offset, -offset*0.5, r"$\mathsf{CO_3^{2-}}$" + '+' + r"$\mathsf{HCO_3^-}$",  
              ha='left', va='center', rotation=0, fontsize=10)
    
    plt.text(0.5+offset+0.5*offset+offset*np.cos(np.pi/30), h+offset*np.tan(np.pi/3)+0.25*np.tan(np.pi/3)+offset*np.sin(np.pi/30), r"$\mathsf{SO_4^{2-} + Cl^-}\Rightarrow$",  
              ha='center', va='center', rotation=60, fontsize=10)
    plt.text(1.5+offset-0.25+offset*np.cos(np.pi/30), h+offset*np.tan(np.pi/3)+0.25*np.tan(np.pi/3)+offset*np.sin(np.pi/30), r"$\Leftarrow\mathsf{Ca^{2+} + Mg^{2+}}$", 
              ha='center', va='center', rotation=-60, fontsize=10)

    plt.text(0.5, h/2+h/4*np.sin(np.pi/4), 'a', ha='center', va='center', rotation=0, fontsize=10)
    plt.text(0.25, h/4*np.sin(np.pi/4), 'b', ha='center', va='center', rotation=0, fontsize=10)
    plt.text(0.75, h/4*np.sin(np.pi/4), 'c', ha='center', va='center', rotation=0, fontsize=10)
    plt.text(0.5, h/2-h/4*np.sin(np.pi/4), 'm', ha='center', va='center', rotation=0, fontsize=10)

    plt.text(1.5+2*offset, h/2+h/4*np.sin(np.pi/4), 'd', ha='center', va='center', rotation=0, fontsize=10)
    plt.text(1.25+2*offset, h/4*np.sin(np.pi/4), 'e', ha='center', va='center', rotation=0, fontsize=10)
    plt.text(1.75+2*offset, h/4*np.sin(np.pi/4), 'f', ha='center', va='center', rotation=0, fontsize=10)
    plt.text(1.5+2*offset, h/2-h/4*np.sin(np.pi/4), 'm', ha='center', va='center', rotation=0, fontsize=10)

    plt.text(1+offset, h+offset*np.tan(np.pi/3)+0.5/(2)*np.tan(np.pi/3), 'A', ha='center', va='center', rotation=0, fontsize=10)
    plt.text(0.75+offset, h+offset*np.tan(np.pi/3), 'B', ha='center', va='center', rotation=0, fontsize=10)
    plt.text(1.25+1*offset, h+offset*np.tan(np.pi/3), 'C', ha='center', va='center', rotation=0, fontsize=10)
    plt.text(1+offset, h+offset*np.tan(np.pi/3)-0.5/(2)*np.tan(np.pi/3), 'D', ha='center', va='center', rotation=0, fontsize=10)

    plt.text(1.5+offset, (1+offset)*np.tan(np.pi/3), 'A: Sulfatadas y/o cloruradas \n     cálcicas y/o magnésicas \nB: Bicarbonatadas cálcicas \n     y/o magnésicas \nC: Cloruradas y/o sulfatadas\n     sódicas \nD: Bicarbonatadas sódicas', ha='left', va='center', rotation=0, fontsize=10)
    plt.text(1.5+offset, (1-1.5*offset)*np.tan(np.pi/3), 'a: Magnésicas \nb: Cálcicas \nc: Sódicas \nm: Mixtas', ha='left', va='bottom', rotation=0, fontsize=10)
    plt.text(1.75+2*offset, (1-1.5*offset)*np.tan(np.pi/3), 'd: Sulfatadas \ne: Bicarbonatadas \nf: Cloruradas \nm: Mixtas', ha='left', va='bottom', rotation=0, fontsize=10)

    plt.text(0.5, -1.25*offset, 'CATIÓN', ha='center', va='bottom', rotation=0, fontsize=10)
    plt.text(1.5+2*offset, -1.25*offset, 'ANIÓN', ha='center', va='bottom', rotation=0, fontsize=10)

    # Fill the water types domain
    ## the left traingle
    #plt.fill([0.25, 0.5, 0.75, 0.25], 
    #         [h/2, 0, h/2, h/2], color = (0.8, 0.8, 0.8), zorder=0)
    ## the right traingle
    #plt.fill([1+2*offset+0.25, 1+2*offset+0.5, 1+2*offset+0.75, 1+2*offset+0.25], 
    #         [h/2, 0, h/2, h/2], color = (0.8, 0.8, 0.8), zorder=0)
    ## the diamond
    #plt.fill([0.5+offset+0.25,0.5+offset+0.25+0.25, 0.5+offset+0.25+0.5, 0.5+offset+0.25+0.25, 0.5+offset+0.25],
    #         [h+offset*np.tan(np.pi/3) - 0.5*np.sin(np.pi/3), offset*np.tan(np.pi/3), h+offset*np.tan(np.pi/3) - 0.5*np.sin(np.pi/3), h+offset*np.tan(np.pi/3), h+offset*np.tan(np.pi/3) - 0.5*np.sin(np.pi/3)], 
    #         color = (0.8, 0.8, 0.8), zorder=0)
    #plt.fill([0.5+offset+0.25, 0.5+offset+0.25+0.25, 0.5+offset+0.25+0.5,0.5+offset+0.25+0.25, 0.5+offset+0.25],
    #         [h+offset*np.tan(np.pi/3) + 0.5*np.sin(np.pi/3), h+offset*np.tan(np.pi/3), h+offset*np.tan(np.pi/3) + 0.5*np.sin(np.pi/3),h+offset*np.tan(np.pi/3) + np.sin(np.pi/3), h+offset*np.tan(np.pi/3) + 0.5*np.sin(np.pi/3)], 
    #         color = (0.8, 0.8, 0.8), zorder=0)
    
    # Convert unit if needed
    if unit == 'mg/L':
        gmol = np.array([ions_WEIGHT['Ca'], 
                         ions_WEIGHT['Mg'], 
                         ions_WEIGHT['Na'], 
                         ions_WEIGHT['K'], 
                         ions_WEIGHT['HCO3'],
                         ions_WEIGHT['CO3'], 
                         ions_WEIGHT['Cl'], 
                         ions_WEIGHT['SO4']])
    
        eqmol = np.array([ions_CHARGE['Ca'], 
                          ions_CHARGE['Mg'], 
                          ions_CHARGE['Na'], 
                          ions_CHARGE['K'], 
                          ions_CHARGE['HCO3'], 
                          ions_CHARGE['CO3'], 
                          ions_CHARGE['Cl'], 
                          ions_CHARGE['SO4']])
    
        tmpdf = df[['Ca', 'Mg', 'Na', 'K', 'HCO3', 'CO3', 'Cl', 'SO4']]
        dat = tmpdf.values
        
        meqL = (dat / abs(gmol)) * abs(eqmol)
        
    elif unit == 'meq/L':
        tmpdf = df[['Ca', 'Mg', 'Na', 'K', 'HCO3', 'CO3', 'Cl', 'SO4']]
        dat = tmpdf.values
        meqL = df[['Ca', 'Mg', 'Na', 'K', 'HCO3', 'CO3', 'Cl', 'SO4']].values
    
    else:
        raise RuntimeError("""
        Currently only mg/L and meq/L are supported.
        Convert the unit if needed.""")
    
    # Calculate the percentages
    sumcat = np.sum(meqL[:, 0:4], axis=1)
    suman = np.sum(meqL[:, 4:8], axis=1)
    cat = np.zeros((dat.shape[0], 3))
    an = np.zeros((dat.shape[0], 3))
    cat[:, 0] = meqL[:, 0] / sumcat                  # Ca
    cat[:, 1] = meqL[:, 1] / sumcat                  # Mg
    cat[:, 2] = (meqL[:, 2] + meqL[:, 3]) / sumcat   # Na+K
    an[:, 0] = (meqL[:, 4] + meqL[:, 5]) / suman     # HCO3 + CO3
    an[:, 2] = meqL[:, 6] / suman                    # Cl
    an[:, 1] = meqL[:, 7] / suman                    # SO4

    # Convert into cartesian coordinates
    cat_x = 0.5 * (2 * cat[:, 2] + cat[:, 1])
    cat_y = h * cat[:, 1]
    an_x = 1 + 2 * offset + 0.5 * (2 * an[:, 2] + an[:, 1])
    an_y = h * an[:, 1]
    d_x = an_y / (4 * h) + 0.5 * an_x - cat_y / (4 * h) + 0.5 * cat_x
    d_y = 0.5 * an_y + h * an_x + 0.5 * cat_y - h * cat_x

    # Plot the scatters
    Labels = []
    for i in range(len(df)):
        if (df.at[i, 'Label'] in Labels or df.at[i, 'Label'] == ''):
            TmpLabel = ''
        else:
            TmpLabel = df.at[i, 'Label']
            Labels.append(TmpLabel)
         
        try:
            if (df['Color'].dtype is np.dtype('float')) or \
                (df['Color'].dtype is np.dtype('int64')):
                vmin = np.min(df['Color'].values)
                vmax = np.max(df['Color'].values)
                cf = plt.scatter(cat_x[i], cat_y[i], 
                                marker=df.at[i, 'Marker'],
                                s=df.at[i, 'Size'], 
                                c=df.at[i, 'Color'], vmin=vmin, vmax=vmax,
                                alpha=df.at[i, 'Alpha'],
                                #label=TmpLabel, 
                                edgecolors='black')
                plt.scatter(an_x[i], an_y[i], 
                            marker=df.at[i, 'Marker'],
                            s=df.at[i, 'Size'], 
                            c=df.at[i, 'Color'], vmin=vmin, vmax=vmax,
                            alpha=df.at[i, 'Alpha'],
                            label=TmpLabel, 
                            edgecolors='black')
                plt.scatter(d_x[i], d_y[i], 
                            marker=df.at[i, 'Marker'],
                            s=df.at[i, 'Size'], 
                            c=df.at[i, 'Color'], vmin=vmin, vmax=vmax,
                            alpha=df.at[i, 'Alpha'],
                            #label=TmpLabel, 
                            edgecolors='black')
                
            else:
                plt.scatter(cat_x[i], cat_y[i], 
                            marker=df.at[i, 'Marker'],
                            s=df.at[i, 'Size'], 
                            c=df.at[i, 'Color'], 
                            alpha=df.at[i, 'Alpha'],
                            #label=TmpLabel, 
                            edgecolors='black')
                plt.scatter(an_x[i], an_y[i], 
                            marker=df.at[i, 'Marker'],
                            s=df.at[i, 'Size'], 
                            c=df.at[i, 'Color'], 
                            alpha=df.at[i, 'Alpha'],
                            label=TmpLabel, 
                            edgecolors='black')
                plt.scatter(d_x[i], d_y[i], 
                            marker=df.at[i, 'Marker'],
                            s=df.at[i, 'Size'], 
                            c=df.at[i, 'Color'], 
                            alpha=df.at[i, 'Alpha'],
                            #label=TmpLabel, 
                            edgecolors='black')
                
        except(ValueError):
            pass
            
    # Creat the legend
    if (df['Color'].dtype is np.dtype('float')) or (df['Color'].dtype is np.dtype('int64')):
        cb = plt.colorbar(cf, extend='both', spacing='uniform',
                          orientation='vertical', fraction=0.025, pad=0.05)
        cb.ax.set_ylabel('$TDS$' + ' ' + '$(mg/L)$', rotation=90, labelpad=-75, fontsize=10)
    
    plt.legend(bbox_to_anchor=(0.15, 0.875), markerscale=1, fontsize=10,
               frameon=False, 
               labelspacing=0.25, handletextpad=0.25,ncol=nc)
    
    # Display the info
    cwd = os.getcwd()
    print("Trilinear Piper plot created. Saving it to %s \n" %cwd)
    
    # Save the figure
    plt.savefig(figname + '.' + figformat, format=figformat,bbox_inches='tight', dpi=300)
    
    return (figname)


