# 🎓 O projeto faz parte de um Challenge do Curso de ETL da Alura

###  Challenge do Curso de ETL faz parte da formação de Data Science da Alura em parceria com a ONE (Oracle Next Education)

<br>

# 📊 Projeto: Análise de Churn - TelecomX BR

Este projeto tem como objetivo realizar uma análise exploratória de dados e identificar fatores que influenciam no cancelamento de clientes (Churn) em uma operadora de telecomunicações. A análise é feita utilizando Python e ferramentas estatísticas e gráficas.

<br>

# 🧩 Sobre o Projeto

O projeto consiste na análise de uma base de dados contendo informações sobre clientes de uma operadora de telecomunicações, com o intuito de entender os padrões relacionados ao Churn (retenção ou cancelamento dos serviços). Para isso, foram utilizadas técnicas de carregamento, tratamento, agregação e visualização de dados.

<br>

# 🛠️ Tecnologias Utilizadas

* Linguagem de Programação: Python 3.11.7
* Ambiente de Desenvolvimento: Jupyter Notebook
* Bibliotecas Utilizadas:
	* pandas, numpy, scipy, matplotlib, seaborn
	* ydata_profiling para geração de relatórios de qualidade dos dados
	* stats, json, requests, warnings

<br>

# 📁 Estrutura do Projeto

```bash
challenge2-data-science/
│
├── TelecomX_BR.ipynb                  # Notebook principal com toda a análise
├── README.md                          # Este arquivo
├── report/
│   ├── telecom_data_report_before.html # Relatório antes do tratamento
│   └── telecom_data_report_after.html  # Relatório após o tratamento
├── scripts/
│   ├── local_tools.py                 # Funções genéricas de apoio
│   └── telecomx_analysis.py           # Funções específicas para análise
└── data/                              # Pasta com o dataset original (não incluída)
```

</br>


# 🧪 Objetivo da Análise

Identificar quais variáveis estão mais fortemente associadas ao Churn de clientes, através de:

* Estatísticas descritivas
* Visualizações gráficas
* Agrupamentos e análises por perfil de cliente
* Comparativos entre clientes ativos e inativos

</br>

# 🔍 Dicionário de Dados

Para acesso ao dicionário de dados disponibilizado para análise e dionário de dados criado após os processos de transformação e agregação acessar arquivo 

TelecomX_dicionario.md

</br>

# 📦 Dependências

Certifique-se de instalar as seguintes dependências:

```python
pip install pandas numpy scipy matplotlib seaborn ydata-profiling jupyter ipykernel
```

</br>

# ▶️ Como Executar o Projeto

1. Clone este repositório:

```bash
git clone https://github.com/jpierre06/challenge2-data-science.git
cd challenge2-data-science
```

2. Instale as dependências conforme listado acima.
3. Abra o notebook Jupyter:

```bash
jupyter lab TelecomX_BR.ipynb
```
4. Execute todas as células para gerar os resultados e visualizações.


</br>

# 📋 Relatórios Gerados

Após a execução do notebook, existe a opção de gerar dois relatórios HTML através da ferramenta ydata_profiling na pasta report/:

* telecom_data_report_before.html: Perfil da base antes do tratamento
* telecom_data_report_after.html: Perfil da base após o tratamento

#### Obs: Por padrão, as duas linhas de código para geração do relatório estão comentadas com '#' no notebook, para geração dos referidos relatório é necessário descomentar as respectivas linhas de código e executar as células

</br>

# 📌 Considerações Finais

Este projeto visa demonstrar habilidades em:

* Manipulação e limpeza de dados
* Visualização de informações
* Interpretação estatística
* Boas práticas de organização de código

É o estudo de uma solução para análise de churn em clientes de telecomunicação, podendo ser expandido futuramente com modelagem preditiva.

</br>

# 📬 Contato

Se você tiver dúvidas, sugestões ou quiser contribuir com melhorias, sinta-se à vontade para entrar em contato ou abrir uma issue no repositório.

### 📧 [Email] jps.data.analise@gmail.com

### 💼 [LinkedIn Profile] https://www.linkedin.com/in/jeanpierresantana