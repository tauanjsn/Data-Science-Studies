import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import sys

import os

print ('Quantidade de argumentos:', len(sys.argv), 'argumentos.')
print ('Lista de argumentos:', sys.argv)
def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,
                       aggfunc=func).unstack().plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    return None
    
def gerador_graficos (mes):
    sinasc = pd.read_csv('SINASC_RO_2019_'+sys.argv[mes]+'.csv')
    print('Data minima: ', sinasc.DTNASC.min())
    print('Data máxima: ', sinasc.DTNASC.max())

    max_data = sinasc.DTNASC.max()[:7]
    print(max_data)
    
    os.makedirs('./output/figs/'+max_data, exist_ok=True)

    plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'count', 'quantidade de nascimento','data de nascimento')
    plt.savefig('./output/figs/'+max_data+'/quantidade de nascimento_'+max_data+'.png')

    plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae','data de nascimento','unstack')
    plt.savefig('./output/figs/'+max_data+'/media idade mae por sexo_'+max_data+'.png')

    plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe','data de nascimento','unstack')
    plt.savefig('./output/figs/'+max_data+'/media peso bebe por sexo_'+max_data+'.png')

    plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median', 'apgar1 mediano','gestacao','sort')
    plt.savefig('./output/figs/'+max_data+'/apgar1 mediano por escolaridade mae_'+max_data+'.png')

    plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio','gestacao','sort')
    plt.savefig('./output/figs/'+max_data+'/media apgar1 por gestacao_'+max_data+'.png')

    plota_pivot_table(sinasc, 'APGAR5', 'GESTACAO', 'mean', 'apgar5 medio','gestacao','sort')
    plt.savefig('./output/figs/'+max_data+'/media apgar5 por gestacao_'+max_data+'.png')
    
meses = [1,2,3,4,5,6,7,8,9,10,11,12]
for args in meses:
    if args < len(sys.argv):
        gerador_graficos(args)
    
    

