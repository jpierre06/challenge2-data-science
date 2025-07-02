import pandas as pd
import numpy as np
import json
import requests

import seaborn as sns
import matplotlib.pyplot as plt

import scripts.local_tools as lt


def carregar_dados_telecomx_normalizado(caminho_arquivo_json: str, imprimir=True):
    ...
    # Fazendo a requisição HTTP
    response = requests.get(caminho_arquivo_json)
    # Verificando se a requisição foi bem-sucedida
    if response.status_code == 200:
        dados_telecom = json.loads(response.text)
    else:
        print("Erro ao acessar o arquivo:", response.status_code)

    df = pd.json_normalize(dados_telecom, sep='_', meta=['customerID', 'Churn'])

    return df


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

    if imprimir:
        num_invalidos = len(df[df['Churn'].isin(lista_valores_invalidos)])
        print(f'\nValores inválidos coluna Churn: {num_invalidos}')
        num_invalidos = len(df[df['account_Charges_Total'].isin(lista_valores_invalidos)])
        print(f'\nValores inválidos coluna account_Charges_Total: {num_invalidos}')

    df.Churn = df.Churn.replace(lista_valores_invalidos, 'No')
    df.account_Charges_Total = df.account_Charges_Total.replace(lista_valores_invalidos, '0')

    if imprimir:
        num_invalidos = len(df[df['Churn'].isin(lista_valores_invalidos)])
        print(f'\nValores inválidos coluna Churn: {num_invalidos}')
        num_invalidos = len(df[df['account_Charges_Total'].isin(lista_valores_invalidos)])
        print(f'\nValores inválidos coluna account_Charges_Total: {num_invalidos}')
    
        # Verificar se existe algum cliente na base que não assina nenhum serviço
        num_inconsistentes = len(df[(df['phone_PhoneService'] == 'No') & (df['internet_InternetService'] == 'No')])
        print(f'\nClientes sem serviços de Telefone e Internet contratados: {num_inconsistentes}')

        num_inconsistentes = len(df[(df['phone_MultipleLines'] == 'No phone service') & (df['phone_PhoneService'] == 'Yes')])
        print(f'\nClientes com múltiplas linhas de Telefone sem serviço de Telefone contratado: {num_inconsistentes}')

    return df


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
    colunas_valores_binarios = []
    for c in df.columns:
        if len(set(df[c].unique()).difference(set([0, 1]))) == 0:
            colunas_valores_binarios.append(c)

    if imprimir:
        for c in colunas_valores_binarios:
            print(f'Coluna: {c}. Quantidade de domínios: {df[c].nunique()}. Valores do domínios: {np.unique(df[c])}\n')

    return df, colunas_valores_binarios


def criar_colunas_derivadas(df):
    
    #   Criação de coluna por faixa tempo de contrato do cliente 
    df['customer_tenure_bins'] = df['customer_tenure'].apply(lambda x: f'{(x // 6) * 6:03}-{(x // 6) * 6 + 5:03}')

    # Informações de contratos mensais
    df['account_Contract_Month'] = np.where(
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
    df['account_Daily'] = df['account_Charges_Monthly'] / 30

    return df


def conversao_tipos(df):
    # Conversão de tipos de dados
    df['Churn'] = df['Churn'].astype(int)
    df['account_Charges_Total'] = pd.to_numeric(df['account_Charges_Total'], errors='coerce')
    df['account_Charges_Monthly'] = pd.to_numeric(df['account_Charges_Monthly'], errors='coerce')
    df['account_Daily'] = pd.to_numeric(df['account_Daily'], errors='coerce')

    return df


def calcular_percentual_churn_categoria(df: pd.DataFrame, categoria:str):
    df_agg = df.groupby([categoria], observed=True).agg(
        customer = ('Churn', 'count'),
        churn = ('Churn', 'sum'),
        perc_churn_customer = ('Churn', lt.apply_percent_category),
    ).reset_index()
    
    df_agg.perc_churn_customer = round(df_agg.perc_churn_customer, 2)
    df_agg.insert(2, 'perc_total_customer', round(df_agg.customer/ np.sum(df_agg.customer) *100, 2))
    
        
    return df_agg


def graf_percentual_chrun(df: pd.DataFrame):
    ...
    # Calcular percentual
    churn_percent = df['Churn'].value_counts(normalize=True).reset_index()
    churn_percent.columns = ['Churn', 'Percent']
    churn_percent['Churn'] = churn_percent['Churn'].map({0: 'Não', 1: 'Sim'})
    churn_percent['Percent'] *= 100

    sns.set(style='whitegrid')
    plt.figure(figsize=(6, 4))
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
    ...
    # Boxplot para Charges Monthly
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    sns.boxplot(x='Churn', y='account_Charges_Monthly', data=df, ax=axes[0])
    axes[0].set_title('Valor Mensal vs Churn')

    # Boxplot para Tenure
    sns.boxplot(x='Churn', y='customer_tenure', data=df, ax=axes[1])
    axes[1].set_title('Tempo de Contrato vs Churn')

    plt.tight_layout()

    # Remover bordas
    for spine in ['top', 'right']:
        plt.gca().spines[spine].set_visible(False)

    return plt


def graf_distribuicao_churn(df: pd.DataFrame):
    ...
    # KDEplot para Charges Monthly e customer_tenure
    plt.figure(figsize=(12, 5))

    # Valor mensal
    plt.subplot(1, 2, 1)
    sns.kdeplot(data=df, x='account_Charges_Monthly', hue='Churn', fill=True)
    plt.title('Distribuição do Valor Mensal por Churn')

    # Tempo de contrato
    plt.subplot(1, 2, 2)
    sns.kdeplot(data=df, x='customer_tenure', hue='Churn', fill=True)
    plt.title('Distribuição do Tempo de Contrato por Churn')

    plt.tight_layout()

    # Remover bordas
    for spine in ['top', 'right']:
        plt.gca().spines[spine].set_visible(False)

    return plt