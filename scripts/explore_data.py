#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Explorar datos I2D - registros sonoros

@author: jsulloa
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def load_format_excel(fname):
    df = pd.read_excel(fname)
    
    cols_idx = ['genus','specificEpithet', 'infraspecificEpithet',
                'Valor de la medida (Calidad Corte)',
                'Valor de la medida (Duración en segundos)',
                'Valor de la medida (Tiempo Inicial en Segundosundos)',
                'Valor de la medida (Tiempo final en Segundosundos)',
                'Valor de la medida (Tipo de Canto)']
    
    
    df = df.loc[:,cols_idx]
    df['sp_name'] = df['genus'] + ' ' + df['specificEpithet']
    return df


df_bolivar = load_format_excel('./Bolivar/final_rrbb_bolivar2017_aves_2018_v2.xlsx')
df_cesar = load_format_excel('./Cesar/final_rrbb_cesar2017_aves_2018.xlsx')
df_guajira = load_format_excel('./Guajira/final_rrbb_guajira2016_aves_2018_v3.xlsx')

df_bolivar['depto'] = 'bolivar'
df_cesar['depto'] = 'cesar'
df_guajira['depto'] = 'guajira'

df_caribe = pd.concat([df_bolivar, df_cesar, df_guajira], axis=0)
idx_nan = df_caribe['Valor de la medida (Tipo de Canto)'].isna()
df_caribe = df_caribe.loc[~idx_nan,:]
## corregir algunas observaciones no tienen tiempo inicio y final. df_caribe.dropna(inplace=True)

# número de especies
num_sp = df_caribe.sp_name.value_counts()
num_sp_plot = 15
xx = num_sp.iloc[0:num_sp_plot]
plt.close('all')


## overview global
fig, ax = plt.subplots(1,1, figsize=[10,5])
ax.barh(np.arange(len(num_sp)), num_sp, height=0.5)
ax.set_yticks([])
ax.set_xticks([])
sns.despine(ax=ax, top=True, left=True, right=True, bottom=True)

## especies con más registros
fig, ax = plt.subplots(1,1, figsize=[10,5])
ax.barh(np.arange(num_sp_plot), xx)
ax.set_yticks([])
ax.set_xlabel('Número de cortes')
ax.axvline(x=20, color='white', lw=0.3)
ax.axvline(x=40, color='white', lw=0.3)
ax.axvline(x=60, color='white', lw=0.3)
for idx, (label, x) in enumerate(xx.iteritems()):
    ax.text(0.1, idx-0.3, label, color='white')
sns.despine(ax=ax, top=True, left=True, right=True, trim=True)

## especies por departamento
num_dept = df_caribe.depto.value_counts()
fig, ax = plt.subplots(1,1, figsize=[5,5])
ax = sns.barplot(x=num_dept.index, y= num_dept)
sns.despine(ax=ax, bottom=True, trim=True)
ax.set_xticklabels(['Bolívar', 'Cesar', 'Guajira'])
ax.set_ylabel('Número de cortes')


