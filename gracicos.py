import pandas as pd
import pydeck as pdk
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import plotly.io as pio

pio.renderers.default = 'browser'


def casos_dengue_ano(dengue19, dengue20, zika_21):

    dengue19_1 = dengue19.groupby(['mes'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2019'}).reset_index() ## SE CREA DATA AGRUPADA por mes
    dengue20_1 = dengue20.groupby(['mes'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2020'}).reset_index() 
    zika_21_1 = zika_21.groupby(['mes'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2021'}).reset_index()
    lista = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
    d = pd.DataFrame(lista,columns=['mes'])
    df = pd.merge(d, dengue19_1, on='mes', how='outer')
    df = pd.merge(df, dengue20_1, on='mes', how='outer')
    df = pd.merge(df,zika_21_1, on = 'mes', how='outer')
    df = df.fillna(0)
    df['TOTAL'] = df.iloc[:,1:].apply(lambda x: sum(x), axis=1)
    
    fig= px.line(df, x='mes', y=['2019','2020','2021'], 
                 color_discrete_sequence=["crimson","chocolate","darkcyan"], width=1250, height=450)
    
    #agregar detalles
    fig.update_layout(
        template='simple_white',
        title_x=0.5,
        legend_title = 'Año',
        xaxis_title= '<b>Meses<b>',
        yaxis_title= '<b>Cantidad de casos por mes <b>'
    ) 
    return fig
    
def provincias_2021(zika_21):
    
    zika_21['provincia_nombre']= zika_21['provincia_nombre'].str.lower()
    zika_21['grupo_edad_desc'] = zika_21['grupo_edad_desc'].str.lower()
    zika_21['grupo_edad_desc']= zika_21['grupo_edad_desc'].replace('de 45 a 64 anos','de 45 a 65 anos')
    lista = ['de 5 a 9 anos','de 10 a 14 anos', 'de 15 a 19 anos','de 20 a 24 anos','de 25 a 34 anos','de 35 a 44 anos','de 45 a 65 anos']
    e = pd.DataFrame(lista,columns=['grupo_edad_desc'])
    zika_edades = zika_21.groupby(['grupo_edad_desc','provincia_nombre'])[['cantidad_casos']].sum().reset_index()
    
    zika_edades = zika_edades.sort_values(by='cantidad_casos', ascending= False)
    zika_edades['grupo_edad_desc']=zika_edades['grupo_edad_desc'].astype('category')
    zika_edades['provincia_nombre']=zika_edades['provincia_nombre'].astype('category')
    zika_ed= zika_edades.head(10).reset_index(drop=True)
    zika_edades1 = pd.merge(e, zika_ed, on='grupo_edad_desc', how='outer')
    zika_edades1
    fig = px.bar(zika_edades1, x = 'grupo_edad_desc', y='cantidad_casos', color = 'provincia_nombre', barmode = 'group', 
                  width=600, height=450, color_discrete_sequence=["darkcyan","coral"]) 
    
    # agregar detalles a la gráfica
    fig.update_layout(
        xaxis_title = 'Grupo edad',
        yaxis_title = 'Cantidad Casos',
        template = 'simple_white',
        title_x = 0.5)

    return fig

def edad_afectada(dengue19, dengue20, zika_21):
    
    dengue19_3 = dengue19.groupby(['departamento_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2019'}).reset_index() ## SE CREA DATA AGRUPADA por mes
    dengue20_3 = dengue20.groupby(['departamento_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2020'}).reset_index() 
    zika_21_3 = zika_21.groupby(['departamento_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2021'}).reset_index()
    df2 = pd.merge(dengue19_3, dengue20_3, on='departamento_nombre', how='outer')
    df2 = pd.merge(df2,zika_21_3, on = 'departamento_nombre', how='outer')
    df2 = df2.fillna(0)
    df2['TOTAL'] = df2.iloc[:,1:].apply(lambda x: sum(x), axis=1)
    df2= df2.sort_values('TOTAL', ascending=False)
    df2 = df2.head(5)
    cnt_ed = df2['TOTAL'].sum()
    
    # hacer la gráfica
    fig = px.pie(df2, values = 'TOTAL', names ='departamento_nombre',
                 hole = .5,
                 color_discrete_sequence = ["coral","crimson","darkcyan","cornflowerblue","purple"], width=700, height=300)
    
    # poner detalles a la gráfica
    fig.update_layout(
        template = 'simple_white',
        title_x = 0.5,
        annotations = [dict(text = str(cnt_ed), x=0.5, y = 0.5, font_size = 20, showarrow = False )])

    return fig    
           
def edad_afectada_2019(dengue19, dengue20, zika_21):
    dengue19_3 = dengue19.groupby(['departamento_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2019'}).reset_index() ## SE CREA DATA AGRUPADA por mes
    dengue20_3 = dengue20.groupby(['departamento_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2020'}).reset_index() 
    zika_21_3 = zika_21.groupby(['departamento_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2021'}).reset_index()
    df2 = pd.merge(dengue19_3, dengue20_3, on='departamento_nombre', how='outer')
    df2 = pd.merge(df2,zika_21_3, on = 'departamento_nombre', how='outer')
    df2 = df2.fillna(0)
    df2['TOTAL'] = df2.iloc[:,1:].apply(lambda x: sum(x), axis=1)
    df2= df2.sort_values('TOTAL', ascending=False)
    df2 = df2.head(5)
    df3= df2.sort_values('2019', ascending=False)
    df3=df3.head(3)
    cnt_ed = df3['2019'].sum()
    
    # hacer la gráfica
    fig = px.pie(df3, values = '2019', names ='departamento_nombre',
                 hole = .5,
                 color_discrete_sequence=["purple", "coral","cornflowerblue"], width=700, height=300)
    
    # poner detalles a la gráfica
    fig.update_layout(
        template = 'simple_white',
        title_x = 0.5,
        annotations = [dict(text = str(cnt_ed), x=0.5, y = 0.5, font_size = 20, showarrow = False )])
   
    return fig
  
def edad_afectada_2020(dengue19, dengue20, zika_21):
    
    dengue19_3 = dengue19.groupby(['departamento_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2019'}).reset_index() ## SE CREA DATA AGRUPADA por mes
    dengue20_3 = dengue20.groupby(['departamento_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2020'}).reset_index() 
    zika_21_3 = zika_21.groupby(['departamento_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2021'}).reset_index()
    df2 = pd.merge(dengue19_3, dengue20_3, on='departamento_nombre', how='outer')
    df2 = pd.merge(df2,zika_21_3, on = 'departamento_nombre', how='outer')
    df2 = df2.fillna(0)
    df2['TOTAL'] = df2.iloc[:,1:].apply(lambda x: sum(x), axis=1)
    df2= df2.sort_values('TOTAL', ascending=False)
    df2 = df2.head(5)
    df4= df2.sort_values('2020', ascending=False)
    df4=df4.head(5)
    cnt_ed = df4['2020'].sum()
    
    # hacer la gráfica
    fig = px.pie(df4, values = '2020', names ='departamento_nombre',
                 hole = .5,
                 color_discrete_sequence = ["coral","crimson","cornflowerblue","darkcyan","purple"],width=700, height=300)
    
    # poner detalles a la gráfica
    fig.update_layout(
        template = 'simple_white',
        title_x = 0.5,
        annotations = [dict(text = str(cnt_ed), x=0.5, y = 0.5, font_size = 20, showarrow = False )])
 
    return fig  
         
def edad_afectada_2021(dengue19, dengue20, zika_21):
    
    dengue19_3 = dengue19.groupby(['departamento_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2019'}).reset_index() ## SE CREA DATA AGRUPADA por mes
    dengue20_3 = dengue20.groupby(['departamento_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2020'}).reset_index() 
    zika_21_3 = zika_21.groupby(['departamento_nombre'])[['cantidad_casos']].count().rename(columns = {'cantidad_casos':'2021'}).reset_index()
    df2 = pd.merge(dengue19_3, dengue20_3, on='departamento_nombre', how='outer')
    df2 = pd.merge(df2,zika_21_3, on = 'departamento_nombre', how='outer')
    df2 = df2.fillna(0)
    df2['TOTAL'] = df2.iloc[:,1:].apply(lambda x: sum(x), axis=1)
    df2= df2.sort_values('TOTAL', ascending=False)
    df2 = df2.head(5)
    df5= df2.sort_values('2021', ascending=False)
    df5=df5.head(5)
    cnt_ed = df5['2021'].sum()
    
    # hacer la gráfica
    fig = px.pie(df5, values = '2021', names ='departamento_nombre',
                 hole = .5,
                 color_discrete_sequence=["coral","darkcyan","crimson","cornflowerblue","purple"], width=700, height=300)
    
    # poner detalles a la gráfica
    fig.update_layout(
        template = 'simple_white',
        title_x = 0.5,
        annotations = [dict(text = str(cnt_ed), x=0.5, y = 0.5, font_size = 20, showarrow = False )])

    return fig  

    
