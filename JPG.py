#!/usr/bin/env python
# coding: utf-8

# ##  Bibliotecas:

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image


# ##  Input Imagens:

# In[5]:


#Barra Lateral
image = Image.open('Logo-Escuro.png')
st.sidebar.image(image)
st.sidebar.markdown('### Definição da Fórmula de Classificação Supervisionada para Daninhas 🌱')
barra_lateral = st.sidebar.empty()
daninha_1 = st.sidebar.file_uploader("🌿Upload Daninha 1:", type=['jpeg','jpg','png'])
daninha_2 = st.sidebar.file_uploader("🌿Upload Daninha 2:", type=['jpeg','jpg','png'])
daninha_3 = st.sidebar.file_uploader("🌿Upload Daninha 3:", type=['jpeg','jpg','png'])

#solo_1 = st.sidebar.file_uploader("🌿Upload Solo 1:", type=['jpeg','jpg','png'])
#solo_2 = st.sidebar.file_uploader("🌿Upload Solo 2:", type=['jpeg','jpg','png'])
#solo_3 = st.sidebar.file_uploader("🌿Upload Solo 3:", type=['jpeg','jpg','png'])

st.title('Daninhas')
col1, col2, col3 = st.columns(3)
col1.image(daninha_1)
col2.image(daninha_2)
col3.image(daninha_3)

#st.title('Solo Exposto e Palhada')
#col1.image(solo_1)
#col2.image(solo_2)
#col3.image(solo_3)


# ##  Ler Pixels das Imagens das Daninhas e transformar os dados em DF:

# In[6]:


# Abre a imagem 1 
img = Image.open(daninha_1)
cores = []
for cor_rgb in img.getdata():
    if cor_rgb not in cores:
        cores.append(cor_rgb)
df1 = pd.DataFrame(cores, columns = ['Red','Green','Blue'])

# Abre a imagem 2 
img = Image.open(daninha_2)
cores2 = []
for cor_rgb in img.getdata():
    if cor_rgb not in cores2:
        cores2.append(cor_rgb)
df2 = pd.DataFrame(cores2, columns = ['Red','Green','Blue'])

# Abre a imagem 3 
img = Image.open(daninha_3)
cores3 = []
for cor_rgb in img.getdata():
    if cor_rgb not in cores3:
        cores3.append(cor_rgb)
df3 = pd.DataFrame(cores3, columns = ['Red','Green','Blue'])


# ##  Tratamento do DF:

# In[8]:


# Juntando os DataFrames Daninhas
result = df1.append([df2, df3])
result= result.drop_duplicates()
result.reset_index(inplace=True, drop=True)
result['index'] = result.index
result['ajuste1'] = result['Red'] - result['Green']
result['ajuste3'] = (result['Blue']) / (result['Red'] + result['Green'] + result['Blue']) * 100


# ##  Gráfico RGB:

# In[9]:


#Gráfico Dados
st.title('Gráfico com todos os Pontos RGB')
fig_RGB, ax = plt.subplots(figsize=(13, 5))
plt.scatter(result['index'], result['Red'], color='Red')
plt.scatter(result['index'], result['Green'], color='Green')
plt.scatter(result['index'], result['Blue'], color='blue')
plt.xlabel('Índice')
plt.ylabel('Valor do Pixel')
st.pyplot(fig_RGB)


# ##  Ajustes Algoritmo D-PP:

# In[11]:


col4, col5 = st.columns(2)

ajuste1 = result['ajuste1'].max() 
ajuste1 = 0 if ajuste1 <= 0 else ajuste1
col4.metric(label="Fator de Ajuste 1️⃣:", value= ajuste1)

ajuste2 = result['ajuste3'].max()
ajuste2 = round(ajuste2, 2)
col5.metric(label=" Fator de Ajuste 2️⃣:", value= ajuste2)

mosaico = st.text_input('💻 Nome do Mosaico no Q-GIS:')
st.markdown('## Fórmula Calculadora Raster Q-GIS:')
st.text(" ' "+str(mosaico)+ "@1' -" + " ' " +str(mosaico)+"@2' <="    +  str(ajuste1)    +  "AND"  +   " ((('"+str(mosaico)+  "@3')" +  "/" +  " (' "+str(mosaico)+ "@1' +" + " ' " + str(mosaico)+"@2'+" + " ' " + str(mosaico)+ "@3'))*100)"  "<="  +  str(ajuste2))


with st.expander("ℹ️ Informações sobre a Fórmula de Classificação"):
     st.write(""" O ortomosaico é uma matriz de 3 dimensões ou três canais, chamada de RGB (Red,Green,Blue), para cada canal os valores dos pixels variam de 0 a 255, no QGIS é apresentado a seguinte configuração (Banda 1 = Vermelho, Banda 2 = Verde, Banda 3 = Azul).
     Para a identificação das daninhas, se procura os pixels  mais verdes no mosaico, esses pixels iram apresentar valores maiores no canal do verde.

A classificação funciona com duas condições: 

1ª CONDIÇÃO: Encontrar os pixels de daninhas

Banda do Vermelho – Banda do Verde  ≤  Fator de Ajuste 1 
      

2ª CONDIÇÃO: Isolar os pixels das daninhas dos pixels de palhada e solo exposto

Banda do Azul / (Banda do Vermelho + Banda do Verde + Banda do Azul)  ≤  Fator de Ajuste 2 
      

Obs: Os valores dos ajustes 1 e 2 variam de mosaico a mosaico
         
     """)
       

