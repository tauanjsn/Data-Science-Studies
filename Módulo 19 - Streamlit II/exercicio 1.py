
import pandas            as pd
import streamlit         as st
import seaborn           as sns
import matplotlib.pyplot as plt
from PIL                 import Image
import os

#Obtendo o diretório do arquivo .py
dir_path = os.path.dirname(os.path.realpath(__file__))

custom_params = {"axes.spines.right": False, "axes.spines.top": False}
#Tema
sns.set_theme(style="ticks", rc=custom_params)

#Configurando os filtros
def multiselect_filter(relatorio, col, selecionados):
    #Se 'all' for selecionado, todas as colunas serão lidas
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)

def main():
    #Informações da página
    st.set_page_config(page_title = 'Telemarketing analisys',
        layout="wide",
        initial_sidebar_state='expanded'
    )
    #Título
    st.write('# Telemarketing analisys')
    st.markdown("---")
    
    #Imagem no topo lateral
    image = Image.open(dir_path + "/Bank-Branding.jpg")
    st.sidebar.image(image)

    #Lendo dados
    bank_raw = pd.read_csv(dir_path + '/bank-additional-full.csv', sep=';')
    bank = bank_raw.copy()

    #Exibindo dataframe
    st.write('## Antes dos filtros')
    st.write(bank_raw.head())

    with st.sidebar.form(key='my_form'):
    
        # IDADES
        max_age = int(bank.age.max())
        min_age = int(bank.age.min())
        idades = st.slider(label='Idade', 
                            min_value = min_age,
                            max_value = max_age, 
                            value = (min_age, max_age),
                            step = 1)


        # PROFISSÕES
        jobs_list = bank.job.unique().tolist()
        jobs_list.append('all')
        jobs_selected =  st.multiselect("Profissão", jobs_list, ['all'])

        # ESTADO CIVIL
        marital_list = bank.marital.unique().tolist()
        marital_list.append('all')
        marital_selected =  st.multiselect("Estado civil", marital_list, ['all'])

        # DEFAULT?
        default_list = bank.default.unique().tolist()
        default_list.append('all')
        default_selected =  st.multiselect("Default", default_list, ['all'])

        
        # TEM FINANCIAMENTO IMOBILIÁRIO?
        housing_list = bank.housing.unique().tolist()
        housing_list.append('all')
        housing_selected =  st.multiselect("Tem financiamento imob?", housing_list, ['all'])

        
        # TEM EMPRÉSTIMO?
        loan_list = bank.loan.unique().tolist()
        loan_list.append('all')
        loan_selected =  st.multiselect("Tem empréstimo?", loan_list, ['all'])

        
        # MEIO DE CONTATO?
        contact_list = bank.contact.unique().tolist()
        contact_list.append('all')
        contact_selected =  st.multiselect("Meio de contato", contact_list, ['all'])

        
        # MÊS DO CONTATO
        month_list = bank.month.unique().tolist()
        month_list.append('all')
        month_selected =  st.multiselect("Mês do contato", month_list, ['all'])

        
        # DIA DA SEMANA
        day_of_week_list = bank.day_of_week.unique().tolist()
        day_of_week_list.append('all')
        day_of_week_selected =  st.multiselect("Dia da semana", day_of_week_list, ['all'])


        bank = (bank.query("age >= @idades[0] and age <= @idades[1]")
                    .pipe(multiselect_filter, 'job', jobs_selected)
                    .pipe(multiselect_filter, 'marital', marital_selected)
                    .pipe(multiselect_filter, 'default', default_selected)
                    .pipe(multiselect_filter, 'housing', housing_selected)
                    .pipe(multiselect_filter, 'loan', loan_selected)
                    .pipe(multiselect_filter, 'contact', contact_selected)
                    .pipe(multiselect_filter, 'month', month_selected)
                    .pipe(multiselect_filter, 'day_of_week', day_of_week_selected)
        )



        submit_button = st.form_submit_button(label='Aplicar')
    
    st.write('## Após os filtros')
    st.write(bank.head())
    st.markdown("---")

    # PLOTS    
    fig, ax = plt.subplots(1, 2, figsize = (5,3))

    bank_raw_target_perc = bank_raw.y.value_counts(normalize = True).to_frame()*100
    bank_raw_target_perc = bank_raw_target_perc.sort_index()
    sns.barplot(x = bank_raw_target_perc.index, 
                y = 'y',
                data = bank_raw_target_perc, 
                ax = ax[0])
    ax[0].bar_label(ax[0].containers[0])
    ax[0].set_title('Dados brutos',
                    fontweight ="bold")
    
    try:
        bank_target_perc = bank.y.value_counts(normalize = True).to_frame()*100
        bank_target_perc = bank_target_perc.sort_index()
        sns.barplot(x = bank_target_perc.index, 
                    y = 'y', 
                    data = bank_target_perc, 
                    ax = ax[1])
        ax[1].bar_label(ax[1].containers[0])
        ax[1].set_title('Dados filtrados',
                        fontweight ="bold")
    except:
        st.error('Erro no filtro')
    
    st.write('## Proporção de aceite')

    st.pyplot(plt)


if __name__ == '__main__':
	main()
    









