import pandas as pd
import numpy as np
import math
import json
import requests

import seaborn as sns
import matplotlib.pyplot as plt
import warnings

import scripts.local_tools as lt


def carregar_dados_telecomx_normalizado(caminho_arquivo_json: str, imprimir=True):
    # Fazendo a requisição HTTP
    response = requests.get(caminho_arquivo_json)
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        dados_telecom = json.loads(response.text)
        df = pd.json_normalize(dados_telecom, sep='_', meta=['customerID', 'Churn'])
        return df    
    else:
        print("Erro ao acessar o arquivo:", response.status_code)
        return None


def extrair_colunas_categoricas(df: pd.DataFrame, quantidade_minima=5, imprimir=True):
    
    colunas_categoricas = []
    for c in df.columns:
        if df[c].nunique() <= quantidade_minima:
            print(f'\nColuna: {c}. Quantidade de domínios: {df[c].nunique()}. Valores do domínios: {np.unique(df[c])}') if imprimir else None
            colunas_categoricas.append(c)

    return colunas_categoricas


def extrair_colunas_numericas(df: pd.DataFrame, colunas_categoricas: list, deletar_colunas:list, imprimir=True):
    
    colunas_numericas = list(set(df.columns).difference(set(colunas_categoricas)))
    for c in deletar_colunas:
        colunas_numericas.remove(c)
    print(colunas_numericas) if imprimir else None

    return colunas_numericas


def perc_registros_churn_invalidados(df: pd.DataFrame, lista_valores_invalidos = ['', ' ', None, 'Nan']):
    num_invalidos = len(df[df['Churn'].isin(lista_valores_invalidos)])
    num_total = len(df)
    return num_invalidos / num_total 


def tratar_valores_invalidados(df: pd.DataFrame, limite_delecao=0.05, imprimir=True):
    lista_valores_invalidos = ['', ' ', None, 'Nan']
    num_invalidos = len(df[df['Churn'].isin(lista_valores_invalidos)])
    num_total = len(df)

    if (num_invalidos / num_total < limite_delecao) & (num_invalidos > 0):
        df = df[~df['Churn'].isin(lista_valores_invalidos)]
        texto_invalidos = f"""
        Foram encontrados {num_invalidos} registros inválidos na variável Churn 
        que representa {(num_invalidos/num_total*100):.2f}% do total de {num_total} registros e está 
        no limite da deleção que é de {(limite_delecao*100):.2f}% e por isso foram deletados.
        """
        print(texto_invalidos) if imprimir else None

    if imprimir:
        print('\nRegistros inválidos antes do tratamento:')
        print(f'\nValores inválidos na variável Churn: {num_invalidos}')
        num_invalidos = len(df[df['account_Charges_Total'].isin(lista_valores_invalidos)])
        print(f'\nValores inválidos na variável account_Charges_Total: {num_invalidos}')

    df.Churn = df.Churn.replace(lista_valores_invalidos, 'No')
    df.account_Charges_Total = df.account_Charges_Total.replace(lista_valores_invalidos, '0')
    df.account_Charges_Total = pd.to_numeric(df.account_Charges_Total, errors='coerce')
    
    df['customer_tenure'] = np.where(
        (df['customer_tenure'] == 0) & (df['account_Charges_Monthly'] != 0), 
        1, 
        df['customer_tenure']
    )

    df['account_Charges_Total'] = np.where(
        (df['account_Charges_Total'] == 0) & (df['customer_tenure'] == 1), 
        df['account_Charges_Monthly'], 
        df['account_Charges_Total']
    )


    if imprimir:
        print('\nRegistros inválidos depois do tratamento:')
        num_invalidos = len(df[df['Churn'].isin(lista_valores_invalidos)])
        print(f'\nValores inválidos na variável Churn: {num_invalidos}')
        num_invalidos = len(df[df['account_Charges_Total'].isin(lista_valores_invalidos)])
        print(f'\nValores inválidos na variável account_Charges_Total: {num_invalidos}')
    
        # Verificar se existe algum cliente na base que não assina nenhum serviço
        num_inconsistentes = len(df[(df['phone_PhoneService'] == 'No') & (df['internet_InternetService'] == 'No')])
        print(f'\nClientes sem serviços de Telefone e Internet contratados: {num_inconsistentes}')

        num_inconsistentes = len(df[(df['phone_MultipleLines'] == 'No phone service') & (df['phone_PhoneService'] == 'Yes')])
        print(f'\nClientes com múltiplas linhas de Telefone sem serviço de Telefone contratado: {num_inconsistentes}')

    return df


def identificar_colunas_valores_binarios(df: pd.DataFrame):
    colunas = []
    for c in df.columns:
        if len(set(df[c].unique()).difference(set([0, 1]))) == 0:
            colunas.append(c)                                         
    return colunas


def tratar_colunas_valores_binarios(df: pd.DataFrame, imprimir=True):
    # Como existe uma coluna de phone_PhoneService, não é necessário detalhar essa informação na coluna phone_MultipleLines. 
    # Sendo possível transformar a mesma em dado binário
    df.phone_MultipleLines = df.phone_MultipleLines.replace('No phone service', 'No')
    
    colunas_internet_additional_service = [
        'internet_OnlineSecurity', 
        'internet_OnlineBackup', 
        'internet_DeviceProtection', 
        'internet_TechSupport', 
        'internet_StreamingTV', 
        'internet_StreamingMovies', 
    ]

    # Como existe uma coluna de internet_InternetService, não é necessário detalhar essa informação nas colunas de cada serviço de internet.
    # Sendo possível transformar a mesma em dado binário
    for c in colunas_internet_additional_service:
        df[c] = df[c].replace('No internet service', 'No')

    colunas_valores_binarios = [
        'Churn',
        'customer_Partner', 
        'customer_Dependents', 
        'phone_PhoneService', 
        'phone_MultipleLines',
        'account_PaperlessBilling', 
        'internet_OnlineSecurity', 
        'internet_OnlineBackup', 
        'internet_DeviceProtection', 
        'internet_TechSupport', 
        'internet_StreamingTV', 
        'internet_StreamingMovies', 
    ]

    # Conversão numerica dos valores binários
    for c in colunas_valores_binarios:
        #print(f'Coluna: {c}. Quantidade de domínios: {df[c].nunique()}. Valores do domínios: {np.unique(df[c])}\n') if imprimir else None
        df[c] = df[c].map({'No': 0, 'Yes': 1})

    # Criação de uma coluna com descrição de serviço de internet para transformar internet_InternetService em coluna com valor binário
    df['internet_Service_Description'] = df['internet_InternetService']
    df['internet_InternetService'] = df['internet_InternetService'].map({'No': 0, 'DSL': 1, 'Fiber optic': 1})

    # Identificação de colunas com valores binários
    colunas_valores_binarios = identificar_colunas_valores_binarios(df)

    if imprimir:
        for c in colunas_valores_binarios:
            print(f'Coluna: {c}. Quantidade de domínios: {df[c].nunique()}. Valores do domínios: {np.unique(df[c])}\n')

    return df, colunas_valores_binarios


def criar_colunas_derivadas(df):
    
    #  Criação de coluna por faixa de tempo de contrato do cliente 
    limite_bins = df.customer_tenure.max() + 13
    bins = list(range(1, limite_bins, 12))
    df['customer_tenure_bins'] = pd.cut(
        df['customer_tenure'],
        bins=bins,
        right=False,  # intervalo fechado à esquerda, aberto à direita
        labels=[f'{str(bins[i]).zfill(3)}-{str(bins[i+1]-1).zfill(3)}' for i in range(len(bins)-1)]
    )

    #  Criação de coluna por faixa de custo mensal do cliente 
    limite_bins = df.account_Charges_Monthly.astype(int).max() + 21
    bins = list(range(1, limite_bins, 20))
    df['account_Charges_Monthly_bins'] = pd.cut(
        df['account_Charges_Monthly'],
        bins=bins,
        right=False,  # intervalo fechado à esquerda, aberto à direita
        labels=[f'R\${str(bins[i]).zfill(3)}-R\${str(bins[i+1]-1).zfill(3)}' for i in range(len(bins)-1)]
    )

    # #  Criação de coluna por faixa de custo mensal do total 
    # # Usando Regra de Sturges
    n = len(df)
    k = int(1 + (10 / 3) * math.log10(n))

    min_val = int(df['account_Charges_Total'].min())
    max_val = int(df['account_Charges_Total'].max())

    # Cria os bins manualmente com base no intervalo total e k
    bin_width = (max_val - min_val) // k + 1
    bins = list(range(min_val, max_val + bin_width, bin_width))

    # Gerar os labels
    labels = [f'R\${str(bins[i]).zfill(5)}-R\${str(bins[i+1]-1).zfill(5)}' for i in range(len(bins)-1)]

    # Aplicar no cut
    df['account_Charges_Total_bins'] = pd.cut(
        df['account_Charges_Total'],
        bins=bins,
        right=False,
        labels=labels
    )

    # Informações de contratos mensais
    df['account_Contract_Monthly'] = np.where(
        (df['account_Contract'].str.lower() == 'month-to-month') , 
        1, 
        0
    )

    colunas_internet_additional_service = [
        'internet_OnlineSecurity', 
        'internet_OnlineBackup', 
        'internet_DeviceProtection', 
        'internet_TechSupport', 
        'internet_StreamingTV', 
        'internet_StreamingMovies', 
    ]
    # Criação de coluna com total de serviços adicionais de internet
    df['additional_InternetService'] = np.sum(df[colunas_internet_additional_service], axis=1)

    # Informações sobre assinaturas combinadas entre Phone e Internet Service
    df['only_PhoneService'] = np.where(
        (df['phone_PhoneService'] == 1) & (df['internet_InternetService'] == 0), 
        1, 
        0
    )

    df['only_InternetService'] = np.where(
        (df['phone_PhoneService'] == 0) & (df['internet_InternetService'] == 1), 
        1, 
        0
    )

    df['both_Phone_InternetService'] = np.where(
        (df['phone_PhoneService'] == 1) & (df['internet_InternetService'] == 1), 
        1, 
        0
    )

    # Criação de coluna de valores diários
    df['account_Charges_Daily'] = df['account_Charges_Monthly'] / 30

    return df


def conversao_tipos(df):
    # Conversão de tipos de dados
    df['Churn'] = df['Churn'].astype(int)
    df['account_Charges_Total'] = pd.to_numeric(df['account_Charges_Total'], errors='coerce')
    df['account_Charges_Monthly'] = pd.to_numeric(df['account_Charges_Monthly'], errors='coerce')
    df['account_Charges_Daily'] = pd.to_numeric(df['account_Charges_Daily'], errors='coerce')

    return df


def calcular_percentual_churn_categoria(df: pd.DataFrame, categoria:str, totalizador:bool=True):
    df_agg = df.groupby([categoria], observed=True).agg(
        customer = ('Churn', 'count'),
        churn = ('Churn', 'sum'),
        perc_churn_customer = ('Churn', lt.apply_percent_category),
    ).reset_index()
    
    
    df_agg.insert(2, 'perc_total_customer', df_agg.customer/ np.sum(df_agg.customer) *100)
    
    if totalizador:
        total_dados = ['Total', df_agg['customer'].sum(), df_agg['perc_total_customer'].sum(), df_agg['churn'].sum()]
        total_col = [categoria, 'customer', 'perc_total_customer', 'churn']
        df_total = pd.DataFrame([total_dados], columns=total_col)
        df_total['perc_churn_customer'] = df_total.churn / df_total.customer * 100        
        df_agg = pd.concat([df_agg, df_total], ignore_index=True)
    
    df_agg.perc_total_customer = round(df_agg.perc_total_customer, 2)
    df_agg.perc_churn_customer = round(df_agg.perc_churn_customer, 2)

    return df_agg


def graf_percentual_chrun(df: pd.DataFrame):
    ...
    # Calcular percentual
    churn_percent = df['Churn'].value_counts(normalize=True).reset_index()
    churn_percent.columns = ['Churn', 'Percent']
    churn_percent['Churn'] = churn_percent['Churn'].map({0: 'Não', 1: 'Sim'})
    churn_percent['Percent'] *= 100

    sns.set(style='whitegrid')
    plt.figure(figsize=(7, 5))
    ax = sns.barplot(data=churn_percent, x='Churn', y='Percent', palette='Blues_d')

    # Adicionar rótulos de valor no topo das barras
    for i in ax.containers:
        ax.bar_label(i, fmt='%.1f%%')

    #Remover bordas
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)

    # Grid Y ao fundo
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, linestyle='--', linewidth=0.7)


    ax.set_title('Percentual de Clientes com Churn')
    ax.set_xlabel('Churn')
    ax.set_ylabel('Percentual (%)')
    ax.set_ylim(0, 100)

    return plt


def graf_boxplot_churn(df: pd.DataFrame):
    # Gráficos com variáveis numéricas pré-definidas
    df = df.copy()
    df.Churn = df.Churn.map({0: 'Não', 1: 'Sim'})

    # Boxplot para Charges Monthly
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.boxplot(x='Churn', y='account_Charges_Monthly', data=df, ax=axes[0])
    axes[0].set_title('Frequência    de Custo Mensal por Churn')
    axes[0].set_xlabel('Churn')
    axes[0].set_ylabel('Custo Mensal')

    # Boxplot para Tenure
    sns.boxplot(x='Churn', y='customer_tenure', data=df, ax=axes[1])
    axes[1].set_title('Frequência de Tempo de Contrato por Churn')
    axes[1].set_xlabel('Churn')
    axes[1].set_ylabel('\n\nTempo de Contrato (meses)')

    plt.tight_layout()

    # Remover bordas
    for spine in ['top', 'right']:
        plt.gca().spines[spine].set_visible(False)

    return plt


def graf_distribuicao_churn(df: pd.DataFrame):
    # Gráficos com variáveis numéricas pré-definidas
    df = df.copy()
    df.Churn = df.Churn.map({0: 'Não', 1: 'Sim'})
    
    # KDEplot para Charges Monthly e customer_tenure
    plt.figure(figsize=(14, 5))

    # Valor mensal
    plt.subplot(1, 2, 1)
    sns.kdeplot(data=df, x='account_Charges_Monthly', hue='Churn', fill=True)
    plt.title('Distribuição de Churn por Custo Mensal')
    plt.xlabel('Custo Mensal')

    # Tempo de contrato
    plt.subplot(1, 2, 2)
    sns.kdeplot(data=df, x='customer_tenure', hue='Churn', fill=True)
    plt.title('Distribuição de Churn por Tempo de Contrato')
    plt.xlabel('Tempo de Contrato (meses)')

    plt.tight_layout()

    # Remover bordas
    for spine in ['top', 'right']:
        plt.gca().spines[spine].set_visible(False)

    return plt


def graf_boxplot_churn_varialvel_numerica(df: pd.DataFrame, variavel_numerica:str, titulo:str, x_label:str='', y_label:str=''):
    # Gráficos com variáveis numéricas pré-definidas
    df = df.copy()
    df.Churn = df.Churn.map({0: 'Não', 1: 'Sim'})

    # Boxplot para variável numérica
    fig, axes = plt.subplots(figsize=(7, 5))
    sns.boxplot(x='Churn', y=variavel_numerica, data=df, ax=axes)
    axes.set_title(titulo)
    axes.set_xlabel('Churn')
    axes.set_ylabel(y_label)

    plt.tight_layout()

    # Remover bordas
    for spine in ['top', 'right']:
        plt.gca().spines[spine].set_visible(False)

    return plt


def graf_distribuicao_churn_varialvel_numerica(df: pd.DataFrame, variavel_numerica:str, titulo:str, x_label:str, y_label:str):
    ...
    warnings.simplefilter(action='ignore', category=FutureWarning)

    df_temp = df.copy()
    df_temp.Churn = df_temp.Churn.map({0: 'Não', 1: 'Sim'})
    
    # KDEplot para variavel_numerica
    plt.figure(figsize=(14, 5))

    # Tempo de contrato
    plt.subplot(1, 2, 2)
    sns.kdeplot(data=df_temp, x=variavel_numerica, hue='Churn', fill=True)
    plt.title(titulo)

    plt.xlabel(x_label)

    plt.tight_layout()

    # Remover bordas
    for spine in ['top', 'right']:
        plt.gca().spines[spine].set_visible(False)

    return plt


def graf_barra_customer_churn(df, var_categorica:str, titulo:str, x_label:str, y_label1:str, y_label2:str, paleta_cor='Blues', converte_bin=False):

    df_temp = calcular_percentual_churn_categoria(df, var_categorica, False)
    if converte_bin:
        df_temp = lt.convert_binary_to_descriptive(df_temp, [var_categorica])
        rotacao=0
    else:
        df_temp[var_categorica] = df_temp[var_categorica].astype(str)
        rotacao=45
    
    top_ylim = lt.round_magnitude(df_temp.customer.max() *1.1)

    plt.figure(figsize=(14, 5))

    # % Base cliente
    plt.subplot(1, 2, 1)
    ax1 = sns.barplot(
        data=df_temp,
        x=var_categorica,
        y='customer',
        palette='Blues'
    )

    # Adicionar rótulos no topo das barras
    for container in ax1.containers:
        ax1.bar_label(container, padding=3)
    
    # Títulos e rótulos
    plt.title(titulo)
    plt.xlabel(x_label)
    plt.xticks(rotation=rotacao)
    plt.ylabel(y_label1)
    plt.ylim(0, top_ylim)

    # % Churn
    ax2 = plt.subplot(1, 2, 2)
    sns.barplot(
        data=df_temp,
        x=var_categorica,
        y='perc_churn_customer',
        palette='Blues'
    )

    # Adicionar rótulos no topo das barras
    for container in ax2.containers:
        ax2.bar_label(container, fmt='%.1f%%', padding=3)

    # Títulos e rótulos
    plt.title(titulo)
    plt.xlabel(x_label)
    plt.xticks(rotation=rotacao)
    plt.ylabel(f'\n\n{y_label2}')
    plt.ylim(0, 100)

    # Ajuste da distância entre os subplots
    plt.subplots_adjust(wspace=0.4)  # Aumenta o espaço horizontal
    plt.tight_layout()
    
    return plt


def graf_matriz_correlacao(df: pd.DataFrame, colunas_numericas: list, titulo:str):
    # Matriz de correlação
    plt.figure(figsize=(10, 6))
    corr = df[colunas_numericas].corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
    
    plt.title(titulo)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)

    # Remover bordas
    for spine in ['top', 'right']:
        plt.gca().spines[spine].set_visible(False)

    return plt