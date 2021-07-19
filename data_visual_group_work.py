#*****************************************************************************
# Allison *****
# M*********
# A*********
# DATA-51100 Statistical Programming
# Spring 2021
# Program Assignment 6 - Visualizing ACS PUMS Data
#*****************************************************************************

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

def load_file(file_name):
    df = pd.read_csv(file_name)
    return df
def visualize_stats(df):
    remove_null = df.HHL.dropna()
    remove_null_hncp = df.HINCP.dropna()
    plt.rcParams.update({'font.size': 18})
    fig = plt.figure(figsize=(40,20))
    
    #Pie chart of Household Languages
    plt.subplot(2,2,1)
    plt.title('Household Languages', ha='center')
    plt.pie(remove_null.value_counts(), startangle=-118)
    plt.legend(['English only','Spanish', 'Other Indo-European','Asian and Pacific Island languages', 'Other'],loc=[-0.25,0.7])
    plt.ylabel("HHL")
    
    #Histogram with KDE plot of Distribution of Household Income
    plt.subplot(2,2,2)
    bins_list = np.logspace(1,7,num=100, endpoint=True, base=10, dtype=None)
    plt.xscale('log')
    plt.hist(remove_null_hncp, density=True, bins=bins_list, color='lightgreen')
    density = gaussian_kde(remove_null_hncp)
    density.covariance_factor = lambda : .10
    density._compute_covariance()
    plt.ticklabel_format(axis='y', style='plain')
    plt.plot(bins_list,density(bins_list),'k--')
    plt.title('Distribution of Household Income')
    plt.xlabel('Household Income($) Log Scaled')
    plt.ylabel('Density')
    plt.grid(True, color = 'k', ls = 'dotted', lw = 0.60 )
    
    #Bar chart of Vehicles Available in Households
    plt.subplot(2,2,3)
    df1=df[['VEH','WGTP']]
    df1 = df1.dropna()
    df2=df1.groupby(['VEH']).sum()
            
    veh_l=df2.index.tolist()
    veh_v=df2.WGTP.tolist()
    
    veh_v1 = []
    for i in veh_v:
        veh_v1.append(i/1000)
    
    plt.bar(veh_l,veh_v1, color='red')
    plt.xticks(np.arange(0,7))
    plt.yticks(np.arange(0,2000,250))
    plt.xlabel('# of Vehicles')
    plt.ylabel('Thousands of Households')
    plt.title('Vehicles Available in Households', ha='center')
  
    #Scatter plot of Property Taxes vs Property Values
    plt.subplot(2,2,4)
    df3 = df[['TAXP','VALP','WGTP','MRGP']]
    removed_df3=df3.dropna()
    l_r = [np.nan, 1]
    count = 50
    for i in range(3,23):
        l_r.append(count)
        count += 50    
    count = 1100
    for i in range(23, 63):
        l_r.append(count)
        count += 100
    count = 5500
    for i in range(63, 65):
        l_r.append(count)
        count += 500
    count = 7000
    for i in range(65, 69):
        l_r.append(count)
        count += 1000
    dict_r = {}
    k = 0
    for i  in range(1,len(l_r)+1):        
        dict_r[i]=l_r[k]
        k+=1
    cm = plt.cm.get_cmap('seismic')
    removed_df3['TAXP']=removed_df3['TAXP'].map(dict_r)
    removed_df3=removed_df3.dropna()
    taxp_y=removed_df3['TAXP'].tolist()
    valp_x = removed_df3['VALP'].tolist()
    sc=plt.scatter(valp_x,taxp_y,marker='o',s=removed_df3['WGTP'], c=removed_df3['MRGP'], cmap=cm, alpha=0.2, linewidths=2)
    cbr = plt.colorbar(sc)
    cbr.set_label('First Mortgage Payment (Monthly $)')
    plt.title('Property Taxes vs Property Values')
    plt.xlabel('Property Value($)')
    plt.ylabel('Taxes($)')
    plt.xlim(0,1200000)
    plt.ticklabel_format(style='plain')
    
    #Save the plot diagram in png
    plt.savefig('pums.png', dpi=300, bbox_inches='tight')
    plt.show()
    
file_name = 'ss13hil.csv'
df = load_file(file_name)
remove_null = df.HHL.dropna()

visualize_stats(df)