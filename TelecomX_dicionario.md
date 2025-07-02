#### Dicionário de dados

* `customerID`: número de identificação único de cada cliente
* `Churn`: se o cliente deixou ou não a empresa 
* `gender`: gênero (masculino e feminino) 
* `SeniorCitizen`: informação sobre um cliente ter ou não idade igual ou maior que 65 anos 
* `Partner`: se o cliente possui ou não um parceiro ou parceira
* `Dependents`: se o cliente possui ou não dependentes
* `tenure`: meses de contrato do cliente
* `PhoneService`: assinatura de serviço telefônico 
* `MultipleLines`: assisnatura de mais de uma linha de telefone 
* `InternetService`: assinatura de um provedor internet 
* `OnlineSecurity`: assinatura adicional de segurança online 
* `OnlineBackup`: assinatura adicional de backup online 
* `DeviceProtection`: assinatura adicional de proteção no dispositivo 
* `TechSupport`: assinatura adicional de suporte técnico, menos tempo de espera
* `StreamingTV`: assinatura de TV a cabo 
* `StreamingMovies`: assinatura de streaming de filmes 
* `Contract`: tipo de contrato
* `PaperlessBilling`: se o cliente prefere receber online a fatura
* `PaymentMethod`: forma de pagamento
* `Charges.Monthly`: total de todos os serviços do cliente por mês
* `Charges.Total`: total gasto pelo cliente

#### Dicionário de dados após tratamento e manipulação dos dados

* `customerID`: número de identificação único de cada cliente
* `Churn`: se o cliente deixou ou não a empresa 
* `customer_gender`: gênero (masculino e feminino) 
* `customer_SeniorCitizen`: informação sobre um cliente ter ou não idade igual ou maior que 65 anos 
* `customer_Partner`: se o cliente possui ou não um parceiro ou parceira
* `customer_Dependents`: se o cliente possui ou não dependentes
* `customer_tenure`:  meses de contrato do cliente
* `phone_PhoneService`: assinatura de serviço telefônico 
* `phone_MultipleLines`: assisnatura de mais de uma linha de telefone 
* `internet_InternetService`: se cliente assina de um provedor internet
* `internet_OnlineSecurity`: assinatura adicional de segurança online
* `internet_OnlineBackup`: assinatura adicional de backup online
* `internet_DeviceProtection`: assinatura adicional de proteção no dispositivo
* `internet_TechSupport`: assinatura adicional de suporte técnico, menos tempo de espera
* `internet_StreamingTV`: assinatura de TV a cabo
* `internet_StreamingMovies`: assinatura de streaming de filmes
* `account_Contract`: tipo de contrato
* `account_PaperlessBilling`: se o cliente prefere receber online a fatura
* `account_PaymentMethod`: forma de pagamento
* `account_Charges_Monthly`: total de todos os serviços do cliente por mês
* `account_Charges_Total`: total gasto pelo cliente
* `internet_Service_Description`: descrição da assinatura de um provedor internet
* `customer_tenure_bins`:  agrupamento de tempo de contrato do cliente a cada 12 meses 
* `account_Charges_Monthly_bins`: agrupamento do total de todos os serviços do cliente a cada 20 reais
* `account_Contract_Monthly`: se cliente tem tipo de assinatura mensal
* `additional_InternetService`: quantidade total de serviços adicionais de internet contratados
* `only_PhoneService`: se cliente assina somente serviço de telefonia
* `only_InternetService`: se cliente assina somente serviço de internet
* `both_Phone_InternetService`: se cliente assina ambos serviços de telefonia e internet
* `account_Daily`: média diária de custo com serviços do cliente baseado no custo mensal considerando o mês comercial de 30 dias
