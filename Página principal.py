# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import plotly.express as px
import re


LOGGER = get_logger(__name__)

PATH = 'data/jorge_martinez_20231220.xlsx'


def run():
    st.set_page_config(
        page_title="Página principal",
        page_icon="👋",
        layout='wide'
    )

    st.title("Nutricionista - Jorge Martinez Zapico")

    st.header('Medidas')



    df_medidas = pd.read_excel(PATH,skiprows=range(1, 9), nrows=18,header=1)

    

    column_names = df_medidas.columns
    new_column_names = {x:x.replace('#NAME?','Fecha').replace('.','-') for x in column_names}

    df_medidas = df_medidas.drop(columns=column_names[1])
    df_medidas = df_medidas.dropna(axis=0)
    df_medidas = df_medidas.rename(columns=new_column_names)

    df_medidas.columns.name = 'Fechas'

    df_medidas['Variables'] = df_medidas['Variables'].str.title()
    df_medidas = df_medidas[df_medidas['Variables'] != 'Talla (M)']

    df_medidas = df_medidas.set_index('Variables')

    
    st.dataframe(df_medidas)

    selected_medida = st.selectbox('Selecciona una medida:',df_medidas.index)
    selected_medida_units = (re.findall(r'\((.*?)\)', selected_medida)[0])
    selected_medida_units = selected_medida_units.lower()

    df_medidas_selected = df_medidas[df_medidas.index==selected_medida] 

    df_medidas_selected_t = df_medidas_selected.transpose()

    col1,col2 = st.columns([0.5,0.5])

    
    with col1:
        
        if 'Peso' in selected_medida:
            delta_color = 'inverse'
        else:
            delta_color = 'normal'
        st.subheader('General')
        previo = df_medidas_selected_t.values.tolist()[-2][0]
        actual = df_medidas_selected_t.values.tolist()[-1][0]
        st.metric("Valor actual", 
                    str(actual)+' '+selected_medida_units, 
                    str(round(actual-previo,3)) +' '+selected_medida_units,
                    delta_color= delta_color)

    with col2:
        st.subheader('Estadísticas')
        subcol1, subcol2 = st.columns(2)
        subcol1.metric("Media", str(df_medidas_selected_t.mean().round(1).values.tolist()[0]) +' '+selected_medida_units)
        subcol2.metric("Mediana",str(df_medidas_selected_t.median().round(1).values.tolist()[0]) +' '+selected_medida_units)
        subcol1.metric("Máximo", str(df_medidas_selected_t.max().round(1).values.tolist()[0]) +' '+selected_medida_units)
        subcol2.metric("Mínimo", str(df_medidas_selected_t.min().round(1).values.tolist()[0]) +' '+selected_medida_units)

    st.subheader('Evolución de '+selected_medida)
    fig = px.line(df_medidas_selected_t,y = selected_medida)

    st.plotly_chart(fig)

    st.header('Cálculos')

    df_calculos = pd.read_excel(PATH,skiprows=range(1, 30), nrows=7,header=1)

    column_names = df_calculos.columns

    new_column_names = {x:y for x,y in zip(column_names,new_column_names.values())}

    df_calculos = df_calculos.drop(columns=column_names[1])
    df_calculos = df_calculos.rename(columns=new_column_names)
    df_calculos = df_calculos.round(2)

    df_calculos.columns.name = 'Fechas'

    df_calculos = df_calculos.set_index('Variables')
      

    st.dataframe(df_calculos)

    selected_calculo = st.selectbox('Selecciona una medida:',df_calculos.index)
    selected_calculo_units = re.findall(r'\((.*?)\)', selected_calculo)
    if len(selected_calculo_units) >0:
        selected_calculo_units = selected_calculo_units[-1]
    else:
        selected_calculo_units = ''
    selected_calculo_units = selected_calculo_units.lower()

    df_calculos_selected = df_calculos[df_calculos.index==selected_calculo] 

    df_calculos_selected_t = df_calculos_selected.transpose()

    col1,col2 = st.columns([0.5,0.5])

    
    with col1:
        
        if 'Masa grasa (kg)' in selected_calculo:
            delta_color = 'inverse'
        else:
            delta_color = 'normal'
        st.subheader('General')
        previo = df_calculos_selected_t.values.tolist()[-2][0]
        actual = df_calculos_selected_t.values.tolist()[-1][0]
        st.metric("Valor actual", 
                    str(actual)+' '+selected_calculo_units, 
                    str(round(actual-previo,3)) +' '+selected_calculo_units,
                    delta_color= delta_color)

    with col2:
        st.subheader('Estadísticas')
        subcol1, subcol2 = st.columns(2)
        subcol1.metric("Media", str(df_calculos_selected_t.mean().round(2).values.tolist()[0]) +' '+selected_calculo_units)
        subcol2.metric("Mediana",str(df_calculos_selected_t.median().round(2).values.tolist()[0]) +' '+selected_calculo_units)
        subcol1.metric("Máximo", str(df_calculos_selected_t.max().round(2).values.tolist()[0]) +' '+selected_calculo_units)
        subcol2.metric("Mínimo", str(df_calculos_selected_t.min().round(2).values.tolist()[0]) +' '+selected_calculo_units)

    st.subheader('Evolución de '+selected_calculo)
    fig = px.line(df_calculos_selected_t,y = selected_calculo)

    st.plotly_chart(fig)



    
    


    

if __name__ == "__main__":
    run()
