'''
Maestría en Ciencia de Datos
Proyecto 1. Descargando datos de la web
Curso Ingeniería de Características
'''

import os
import urllib.request
import datetime
import zipfile
import requests
import pandas as pd

# Datos de población y vivienda en Sonora del INEGI  
ccpv_INEGI_url = 'https://www.inegi.org.mx/contenidos/masiva/indicadores/programas/ccpv/2020/cpv_26_xlsx.zip'
ccpv_INEGI_file = 'ccpv_INEGI'
# Datos de delitos de Sonora del INEGI
del_INEGI_url = 'https://www.inegi.org.mx/contenidos/masiva/indicadores/temas/delitos/delitos_26_xlsx.zip'
del_INEGI_file = 'del_INEGI'
# Datos de pobreza de Sonora de DataMexico API
po_API_url = 'https://dev-api.datamexico.org/tesseract/data.jsonrecords?State=26&cube=coneval_poverty&drilldowns=Municipality%2CYear&measures=Poverty%2CExtreme+Poverty%2CModerate+Poverty%2CPopulation+No+Vulnerable%2CEducational+Backwardness%2CDeprivation+Quality+Housing+Spaces%2CDeprivation+Health+Services%2CDeprivation+Social+Security%2CDeprivation+Basic+Services+Housing%2CDeprivation+Food+Access%2CPopulation+with+at+least+1+Social+Lack%2CPopulation+with+at+least+3+Social+Lacks%2CIncome+below+Welfare+Line%2CIncome+below+Min+Welfare+Line&parents=false&sparse=false'
po_API_file = 'po_API'
# Dirección de los datasets en el proyecto
subdir_zip = 'datasets_zip/'
subdir = 'datasets/'
# Diccionario con las url y dir de los datasets de INEGI (no son por medio de API)
data_dict = {
    ccpv_INEGI_file : ccpv_INEGI_url,
    del_INEGI_file : del_INEGI_url
}
# Descarga y extración de los datos del diccionario 
for data in data_dict:
    # Creación de archivo con metadatos de los datasets
    if not os.path.exists('info.txt'):
        with open('info.txt', 'w') as f:
            f.write("Archivos sobre poblacion, vivienda, pobreza y delitos en Sonora, Mexico.\n")
            info = """
      Los datos de poblacion y vivienda corresponden al Censo de Poblacion y Vivienda (2010, 2015, 2020)
    realizado por INEGI, y cuenta con informacion sobre porcentajes de viviendas de los municipios 
    de Sonora, poblacion y algunas de sus caracteristicas demograficas, socioeconomicas y culturales.
            
      Los datos de delitos registrados corresponden al Censo Nacional de Imparticion de Justicia Estatal
    (2011, 2012, 2013, 2014, 2015) realizado por INEGI, y cuenta con informacion estadistica y geografica
    sobre los delitos registrados por el gobierno Estatal del Sonora, dividido por minicipios.
            
      Los datos de pobreza corresponden al Consejo Nacional de Evaluacion de la Politica de Desarrollo
    Social (CONEVAL) y fueron accedidos a traves de DataMexico. Corresponden a censos de 2010, 2015 y 2020.
            
            """
            f.write(info + '\n')
            f.write("Descargado el " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    if not os.path.exists(subdir_zip + data + '.zip'):  # Comprueba si el archivo existe
        if not os.path.exists(subdir_zip):  # Comprueba si el directorio ya existe
            os.makedirs(subdir_zip)  # Crea el directorio en subdir_zip
        if not os.path.exists(subdir):  # Comprueba si el directorio ya existe
            os.makedirs(subdir)  # Crea el directorio en subdir
        urllib.request.urlretrieve(data_dict[data], subdir_zip + data + '.zip')  # Descarga los datos de la URL
        with zipfile.ZipFile(subdir_zip + data + '.zip', "r") as zip_ref:
            zip_ref.extractall(subdir + data) # Extrae el archivo zip descargado
        with open('info.txt', 'a') as f:
            f.write("Desde: " + data_dict[data] + "\n")
            f.write("Nombre: " + data + "\n")

# Descarga de datos de DataMexico API
main_session = requests.Session() # Dummy request para generar cookies
response = requests.get(po_API_url)
# Guardar los datos de la API en archivo csv
po_df = pd.json_normalize(response.json(),'data')
if not os.path.exists(subdir + po_API_file + '.csv'):  # Comprueba si el archivo existe
    if not os.path.exists(subdir + po_API_file):  # Comprueba si el directorio ya existe
        os.makedirs(subdir + po_API_file)
    po_df.to_csv(subdir + po_API_file + '/' + po_API_file + '.csv')
    with open('info.txt', 'a') as f:
        f.write("Desde: " + po_API_url + "\n")
        f.write("Nombre: " + po_API_file + "\n")