import streamlit as st
import pandas as pd
import numpy as np

#Definindo título
st.title('Viagens de Uber em NYC')

#Carregando dados
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data #Comando para armazenar dados em cache

#Função para ler os dados
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Mensagem de carregamento de dados
data_load_state = st.text('Carregando dados...')
# Número de dados a ser lido
data = load_data(10000)
# Mensagem para quando os dados carregarem
data_load_state.text("Pronto! (using st.cache_data)")

#Checkbox para mostrar tabela de dados
if st.checkbox('Mostrar dados crús'):
    st.subheader('Dados crús')
    st.write(data)

#Subtítulo
st.subheader('Número de viagens por hora')

#Gráfico com quantidade de viagens por hora
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]


st.bar_chart(hist_values)

#Barra deslizante para definir horário desejado
hour_to_filter = st.slider('Hora', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
#Filtragem de dados de acordo com o horário escolhido no slider
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
#Subtítulo
st.subheader(f'Mapa de todas as viagens às {hour_to_filter}:00')
#Mapa com localizações das viagens
st.map(filtered_data)



