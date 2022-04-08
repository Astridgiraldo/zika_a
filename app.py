#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# streamlit run C:\Users\Daniela\Desktop\dashboard\app.py
"""


@author: Daniela Lopez, Daniela Giraldo
"""

# Importar paquetes
import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import base64
import gracicos as gr

dengue_19 = pd.read_csv('Bases/dengue_2019.csv')
dengue_20 = pd.read_csv('Bases/dengue_2020.csv')
zika_21 = pd.read_csv('Bases/zika_final.csv')


# Utilizar la página completa en lugar de una columna central estrecha
st.set_page_config(layout="wide")

# Título principal, h1 denota el estilo del título 1
st.markdown("<h1 style='text-align: center; color: #145A32 ;'> 🏦 Casos de Dengue en Argentina 🦟 </h1>", unsafe_allow_html=True)

# Función para importar datos
@st.cache(persist=True) # Código para que quede almacenada la información en el cache
def load_data(url):
    df = pd.read_csv(url) # leer datos
    df['OCCUR_DATE'] = pd.to_datetime(df['OCCUR_DATE']) # convertir fecha a formato fecha
    df['OCCUR_TIME'] = pd.to_datetime(df['OCCUR_TIME'], format='%H:%M:%S') # convertir hora a formato fecha
    df['YEAR'] = df['OCCUR_DATE'].dt.year # sacar columna con año
    df['HOUR'] = df['OCCUR_TIME'].dt.hour # sacar columna con hora
    df['YEARMONTH'] = df['OCCUR_DATE'].dt.strftime('%Y/%m') # sacar columna con año/mes
    df.columns = df.columns.map(str.lower) # convertir columnas a minúscula
    
    return df

# Función para obtener link de descarga
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="datos.csv">Descargar archivo csv</a>'
    return href



#---------------------------------------------------------------------
st.markdown("<h2 style='text-align: center; color: #196F3D;'> Mayor casos registrados </h2>", unsafe_allow_html=True)

# Generar espacio entre el título y los indicadores
st.markdown("<h3 </h3>", unsafe_allow_html=True)

# Dividir el layout en cuatro partes
c1, c2, c3, c4 = st.columns((1,1,1,1))

## Primer markdown
c1.markdown("<h3 style='text-align: left; color: #1E8449 ;'> Mes </h3>", unsafe_allow_html=True)

# Organizar data

dengue19_1 = dengue_19.groupby(['mes'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2019'}).reset_index() ## SE CREA DATA AGRUPADA por mes
dengue20_1 = dengue_20.groupby(['mes'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2020'}).reset_index() 
zika_21_1 = zika_21.groupby(['mes'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2021'}).reset_index()
lista = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
d = pd.DataFrame(lista,columns=['mes'])
df = pd.merge(d, dengue19_1, on='mes', how='outer')
df = pd.merge(df, dengue20_1, on='mes', how='outer')
df = pd.merge(df,zika_21_1, on = 'mes', how='outer')
df = df.fillna(0)
df['TOTAL'] = df.iloc[:,1:].apply(lambda x: sum(x), axis=1)
df= df.sort_values(by='TOTAL', ascending= False)
y = df.iloc [0, 4]
m = df.iloc [0, 0]
y = int(y)
y1=sum(df.TOTAL)
a = (y/y1)*100
a = round(a,2)

# Enviar a streamlit
c1.text('Mes: '+str(m))
c1.text('Casos: '+ str(y) +', '+str(a)+'%')

## Segundo markdown
c2.markdown("<h3 style='text-align: left; color: #1E8449;'> Edad </h3>", unsafe_allow_html=True)

# Organizar data
dengue20 = dengue_20.rename(columns = { 'grupo_edad_desc': 'grupo_edad'})
dengue20 = dengue_20.rename(columns = { 'grupo_edad_id': 'grupo_edad_desc'})
dengue19_2 = dengue_19.groupby(['grupo_edad_desc'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2019'}).reset_index() ## SE CREA DATA AGRUPADA por mes
dengue20_2 = dengue_20.groupby(['grupo_edad_desc'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2020'}).reset_index() 
zika_21_2 = zika_21.groupby(['grupo_edad_desc'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2021'}).reset_index()
df1 = pd.merge(dengue19_2, dengue20_2, on='grupo_edad_desc', how='outer')
df1 = pd.merge(df1,zika_21_2, on = 'grupo_edad_desc', how='outer')
df1 = df1.fillna(0)
df1['TOTAL'] = df1.iloc[:,1:].apply(lambda x: sum(x), axis=1)
df1= df1.sort_values('TOTAL', ascending=False)
df1['grupo_edad_desc']=df1['grupo_edad_desc'].replace(['de 45 a 65 anos', 'de 45 a 64 anos'], 'de 45 a 64 anos')
df1['grupo_edad_desc']=df1['grupo_edad_desc'].replace(['posneonato (29 hasta 365 dias)', 'posneonato (de 29 a 365 dias)'], 'posneonato (de 29 a 365 dias)')
df1['grupo_edad_desc']=df1['grupo_edad_desc'].replace(['posneonato (de 29 a 365 días)', 'posneonato (de 29 a 365 dias)'], 'posneonato (de 29 a 365 dias)')
lista = ['neonato (hasta 28 dias)','posneonato (de 29 a 365 dias)','de 13 a 24 meses','de 2 a 4 anos','de 5 a 9 anos','de 10 a 14 anos','de 15 a 19 anos','de 20 a 24 anos','de 25 a 34 anos','de 35 a 44 anos','de 45 a 64 anos','mayores de 65 anos']
d = pd.DataFrame(lista,columns=['grupo_edad_desc'])
df1 = pd.merge(d, df1, on='grupo_edad_desc', how='outer')
df1= df1.sort_values(by='TOTAL', ascending= False)
y2 = df1.iloc [0, 4]
e = df1.iloc [0, 0]
y2 = int(y2)
y3=sum(df1.TOTAL)
a1 = (y2/y3)*100
a1 = round(a1,2)


# Enviar a streamlit
c2.text('Rango edad: '+str(e))
c2.text('Casos: '+ str(y2) +', '+str(a1)+'%')

## Tercer markdown
c3.markdown("<h3 style='text-align: left; color: #1E8449 ;'> Provincia </h3>", unsafe_allow_html=True)

# Organizar data
dengue19_4 = dengue_19.groupby(['provincia_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2019'}).reset_index() ## SE CREA DATA AGRUPADA por mes
dengue20_4 = dengue_20.groupby(['provincia_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2020'}).reset_index() 
zika_21_4 = zika_21.groupby(['provincia_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2021'}).reset_index()
df1 = pd.merge(dengue19_4, dengue20_4, on='provincia_nombre', how='outer')
df1 = pd.merge(df1,zika_21_4, on = 'provincia_nombre', how='outer')
df1 = df1.fillna(0)
df1['TOTAL'] = df1.iloc[:,1:].apply(lambda x: sum(x), axis=1)
df1= df1.sort_values('TOTAL', ascending=False)
p = df1.iloc [0, 0]
y2 = df1.iloc [0, 4]
y2 = int(y2)
y3=sum(df1.TOTAL)
a1 = (y2/y3)*100
a1 = round(a1,2)

# Enviar a streamlit
c3.text('Provincia: '+str(p))
c3.text('Casos: '+ str(y2) +', '+str(a1)+'%')



## Cuarto markdown
c4.markdown("<h3 style='text-align: left; color: #1E8449 ;'> departamento </h3>", unsafe_allow_html=True)

# Organizar data
dengue19_3 = dengue_19.groupby(['departamento_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2019'}).reset_index() ## SE CREA DATA AGRUPADA por mes
dengue20_3 = dengue_20.groupby(['departamento_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2020'}).reset_index() 
zika_21_3 = zika_21.groupby(['departamento_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2021'}).reset_index()
df2 = pd.merge(dengue19_3, dengue20_3, on='departamento_nombre', how='outer')
df2 = pd.merge(df2,zika_21_3, on = 'departamento_nombre', how='outer')
df2 = df2.fillna(0)
df2['TOTAL'] = df2.iloc[:,1:].apply(lambda x: sum(x), axis=1)
df2= df2.sort_values('TOTAL', ascending=False)
df2 = df2.head(5)
d = df2.iloc [0, 0]
y2 = df2.iloc [0, 4]
y2 = int(y2)
y3=sum(df1.TOTAL)
a1 = (y2/y3)*100
a1 = round(a1,2)

# Enviar a streamlit
c4.text('Departamento: '+str(d))
c4.text('Casos: '+ str(y2) +', '+str(a1)+'%')



# Dividir el layout en dos partes
c1, c2= st.columns((1,1)) # Entre paréntesis se indica el tamaño de las columnas

# Hacer código de la primera columna (Mapa sencillo):
c1.markdown("<h3 style='text-align: center; color: #145A32;'> ¿Cuales fueron las  provincias mas afectadas en el 2021 y en que edades se presentaron? </h3>", unsafe_allow_html=True)
fig = gr.provincias_2021(zika_21)
c1.plotly_chart(fig)
#year = c1.slider('Año en el que ocurrió el suceso', 2006, 2020) # Crear variable que me almacene el año seleccionado
#c1.map(df[df['year']==year][['latitude', 'longitude']].dropna()) # Generar mapa

# Hacer código de la segunda columna:
c2.markdown("<h3 style='text-align: center; color: #145A32;'> ¿Cuales son las edades mas afectadas por el dengue? </h3>", unsafe_allow_html=True)

# Generar grafica
dengue20 = dengue_20.rename(columns = { 'grupo_edad_desc': 'grupo_edad'})
dengue20 = dengue_20.rename(columns = { 'grupo_edad_id': 'grupo_edad_desc'})
dengue19_2 = dengue_19.groupby(['grupo_edad_desc'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2019'}).reset_index() ## SE CREA DATA AGRUPADA por mes
dengue20_2 = dengue_20.groupby(['grupo_edad_desc'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2020'}).reset_index() 
zika_21_2 = zika_21.groupby(['grupo_edad_desc'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2021'}).reset_index()
df1 = pd.merge(dengue19_2, dengue20_2, on='grupo_edad_desc', how='outer')
df1 = pd.merge(df1,zika_21_2, on = 'grupo_edad_desc', how='outer')
df1 = df1.fillna(0)
df1['TOTAL'] = df1.iloc[:,1:].apply(lambda x: sum(x), axis=1)
df1= df1.sort_values('TOTAL', ascending=False)
df1['grupo_edad_desc']=df1['grupo_edad_desc'].replace(['de 45 a 65 anos', 'de 45 a 64 anos'], 'de 45 a 64 anos')
df1['grupo_edad_desc']=df1['grupo_edad_desc'].replace(['posneonato (29 hasta 365 dias)', 'posneonato (de 29 a 365 dias)'], 'posneonato (de 29 a 365 dias)')
df1['grupo_edad_desc']=df1['grupo_edad_desc'].replace(['posneonato (de 29 a 365 días)', 'posneonato (de 29 a 365 dias)'], 'posneonato (de 29 a 365 dias)')
lista = ['neonato (hasta 28 dias)','posneonato (de 29 a 365 dias)','de 13 a 24 meses','de 2 a 4 anos','de 5 a 9 anos','de 10 a 14 anos','de 15 a 19 anos','de 20 a 24 anos','de 25 a 34 anos','de 35 a 44 anos','de 45 a 64 anos','mayores de 65 anos']
d = pd.DataFrame(lista,columns=['grupo_edad_desc'])
df1 = pd.merge(d, df1, on='grupo_edad_desc', how='outer')

#Crear grafica
fig = px.bar(df1, x = 'grupo_edad_desc', y='TOTAL',
             color_discrete_sequence=["cadetblue"])

# agregar detalles a la gráfica
fig.update_layout(
    xaxis_title = 'Edad',
    yaxis_title = 'Total casos registrados',
    template = 'simple_white',
    title_x = 0.5,
   )

# enviar grafica a streamlit
c2.plotly_chart(fig)
  


#---------------------------------------------------------------------
# Título de la siguiente sección
st.markdown("<h3 style='text-align: center; color: #145A32;'> ¿Cómo ha sido la evolución de los casos de Dengue en Argentina? </h3>", unsafe_allow_html=True)


# Generar gráfica
fig = gr.casos_dengue_ano(dengue_19, dengue_20, zika_21)

# Editar gráfica
fig.update_layout(
        title_x=0.5,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template = 'simple_white',
        xaxis_title="<b>Meses<b>",
        yaxis_title='<b>Cantidad de casos<b>',
        legend_title_text='',
        
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.65))

# Enviar gráfica a streamlit
st.plotly_chart(fig)

#---------------------------------------------------------------------

# Dividir siguiente sección
c4, c5 = st.columns((1,1))

################ ---- Primera Gráfica

# Definir título
c4.markdown("<h3 style='text-align: center; color: #145A32 ;'> ¿Cual fue el departamento mas afectado en los tres ultimos años? </h3>", unsafe_allow_html=True)

# Figura
fig = gr.edad_afectada(dengue_19, dengue_20, zika_21)


# Enviar gráfica a streamlit
c4.plotly_chart(fig)

################ ---- Segunda Gráfica


# Definir título
c5.markdown("<h3 style='text-align: center; color: #145A32;'>¿Cual fue el departamento mas afectado en el 2019?</h3>", unsafe_allow_html=True)

# Figura
fig = gr.edad_afectada_2019(dengue_19, dengue_20, zika_21)



# Enviar gráfica a streamlit
c5.plotly_chart(fig)

################ ---- Tercera Gráfica

# Dividir siguiente seccion
#---------------------------------------------------------------------
c6, c7 = st.columns((1,1))
# Definir título
c6.markdown("<h3 style='text-align: center; color: #145A32;'> ¿Cual fue el departamento mas afectado en el 2020? </h3>", unsafe_allow_html=True)

# Figura
fig = gr.edad_afectada_2020(dengue_19, dengue_20, zika_21)

# Enviar gráfica a streamlit
c6.plotly_chart(fig)

################ ---- Cuarta Gráfica

# Definir título
c7.markdown("<h3 style='text-align: center; color: #145A32;'> ¿Cual fue el departamento mas afectado en el 2021? </h3>", unsafe_allow_html=True)

# Figura
fig = gr.edad_afectada_2021(dengue_19, dengue_20, zika_21)

# Enviar gráfica a streamlit
c7.plotly_chart(fig)

#------------------------------------

