#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Este documento describe un paso a paso para usar anotaciones y registros sonoros 
para crear un set de datos fáciles de usar en un flujo de trabajo de Machine 
Learning. Las anotaciones siguen el formato Darwin Core de eventos de monitoreo 
y están alojados en la infraestructura de de datos.

"""
import pandas as pd
import librosa
from os import path

def load_format_excel(fname):
    df = pd.read_excel(fname)
    
    cols_idx = ['genus','specificEpithet', 'record number',
                'Valor de la medida (Calidad Corte)',
                'Valor de la medida (Duración en segundos)',
                'Valor de la medida (Tiempo Inicial en Segundosundos)',
                'Valor de la medida (Tiempo final en Segundosundos)',
                'Valor de la medida (Tipo de Canto)']
    
    
    df = df.loc[:,cols_idx]
    df['sp_name'] = df['genus'] + ' ' + df['specificEpithet']
    return df


# Set variables
path_annot = '../annotations/test.xlsx'
path_dir_save = '../audio_regions/'
path_audio = '../audio/'
path_metadata = '../audio_regions/audio_metadata.csv'
troom = 1 # room before and after audio region in seconds
fs = 22050
# --

# Load data and remove empty rows
df = load_format_excel(path_annot)
df = df.loc[df['record number'].notna(),:]

# Create a new column with filename to be saved
df.reset_index(inplace=True)
df['index'] = df['record number'].str.slice(0,3).str.upper()+df['index'].apply(lambda x: str(x).zfill(3))
df['fname_save'] = df['genus']+'_'+df['specificEpithet']+'_'+df['index']+'.wav'

# Group by 'record number' which is the name of the long audio recording
gpby = df.groupby('record number')

# For each group of annotations in audio files
for fname, df_gp in gpby:
    audio_fname = path_audio + fname
    if path.exists(audio_fname):
        print('Loading file', audio_fname)
        s, fs = librosa.load(audio_fname, sr=fs)
        
    else:
        print('File not found, skipping:\n', audio_fname)
    # For each annotation
    for idx, row in df_gp.iterrows():
        print('Processing: ', row.fname_save)
        # segment and save audio
        tlims = [int(row['Valor de la medida (Tiempo Inicial en Segundosundos)']*fs), 
                 int(row['Valor de la medida (Tiempo final en Segundosundos)']*fs)]
        s_cut = s[tlims[0]-troom*fs:tlims[1]+troom*fs]
        librosa.output.write_wav(y=s_cut,
                                 path=path_dir_save+row.fname_save,
                                 sr=fs)
    