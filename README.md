# Projeto de Análise e Previsão de Consumo Energético

Este projeto consiste em uma API desenvolvida em Flask que realiza análises de dados de consumo energético, gera previsões e fornece insights para otimizar o uso de energia. A API oferece diversos endpoints para acessar análises estatísticas, previsões e recomendações baseadas em dados de sensores IoT.

## Sumário

- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Execução do Projeto](#execução-do-projeto)
- [Acessando a Documentação Swagger](#acessando-a-documentação-swagger)
- [Descrição dos Endpoints da API](#descrição-dos-endpoints-da-api)

## Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em sua máquina:

- Python 3.7 ou superior
- Pip (gerenciador de pacotes do Python)
- Virtualenv (opcional, mas recomendado)

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu_usuario/seu_repositorio.git
   cd seu_repositorio
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**

   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual:**

   - No Windows:

     ```bash
     venv\Scripts\activate
     ```

   - No Linux/MacOS:

     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

   *Certifique-se de que o arquivo `requirements.txt` contém todas as dependências necessárias, como Flask, Pandas, NumPy, StatsModels, Scikit-learn e Flasgger.*

5. **Organize os dados:**

   - Certifique-se de que os arquivos de dados `powerlytic.csv` e `powerlytic_train.csv` estão presentes no diretório raiz do projeto.
   - Crie uma pasta chamada `sensores` no diretório raiz e adicione os arquivos CSV correspondentes aos sensores de eletrodomésticos. Cada arquivo deve conter dados de consumo com uma coluna chamada `power`.

## Execução do Projeto

Para iniciar a aplicação Flask, execute o seguinte comando no terminal:

```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000/`.

## Acessando a Documentação Swagger

A API utiliza o Flasgger para fornecer uma interface interativa de documentação e teste dos endpoints.

- Acesse a documentação Swagger em: `http://localhost:5000/apidocs/`

Nesta interface, você pode visualizar detalhes sobre cada endpoint, seus parâmetros e testar as chamadas diretamente pelo navegador.

## Descrição dos Endpoints da API

### 1. `/correlations` [GET]

**Descrição:** Obtém a matriz de correlação entre as variáveis relevantes do conjunto de dados.

**Resposta de Sucesso (200):**

- `data`: Dicionário contendo a matriz de correlação entre as variáveis.

### 2. `/hourly_consumption` [GET]

**Descrição:** Retorna o consumo horário médio de eletrodomésticos e luzes.

**Resposta de Sucesso (200):**

- `data`: Lista de dicionários com o consumo médio por hora.

### 3. `/compare_months` [GET]

**Descrição:** Compara o consumo total entre dois meses especificados.

**Parâmetros:**

- `month1` (int, obrigatório): Primeiro mês (1 a 12).
- `year1` (int, obrigatório): Ano do primeiro mês.
- `month2` (int, obrigatório): Segundo mês (1 a 12).
- `year2` (int, obrigatório): Ano do segundo mês.

**Resposta de Sucesso (200):**

- `data`: Dicionário com os consumos totais de cada mês e a variação percentual entre eles.

### 4. `/calculate_appliance_contribution` [GET]

**Descrição:** Calcula a contribuição de cada eletrodoméstico no consumo total de energia.

**Resposta de Sucesso (200):**

- `data`: Dicionário contendo a contribuição média de potência e a porcentagem de cada eletrodoméstico.

### 5. `/generate_tip` [GET]

**Descrição:** Gera dicas personalizadas para o usuário visando a redução do consumo energético com base nos dados atuais.

**Resposta de Sucesso (200):**

- `tips`: Lista de dicas e recomendações para otimização do consumo.

### 6. `/get_prediction` [GET]

**Descrição:** Gera previsões univariadas do consumo de energia para os próximos 30 dias utilizando um modelo SARIMA.

**Resposta de Sucesso (200):**

- `data`: Lista de dicionários com as datas e os valores previstos de consumo.

### 7. `/compare_weeks` [GET]

**Descrição:** Compara o consumo total entre duas semanas especificadas.

**Parâmetros:**

- `week1` (int, obrigatório): Número da primeira semana (1 a 53).
- `year1` (int, obrigatório): Ano da primeira semana.
- `week2` (int, obrigatório): Número da segunda semana (1 a 53).
- `year2` (int, obrigatório): Ano da segunda semana.

**Resposta de Sucesso (200):**

- `data`: Dicionário com os consumos totais de cada semana e a variação percentual entre elas.

### 8. `/generate_multivariate_prediction` [GET]

**Descrição:** Gera previsões multivariadas do consumo de energia para os próximos 30 dias utilizando um modelo SARIMAX com variáveis exógenas.

**Resposta de Sucesso (200):**

- `data`: Lista de dicionários com as datas e os valores previstos de consumo.

### 9. `/evaluate_models` [GET]

**Descrição:** Avalia e compara o desempenho dos modelos de previsão univariado (SARIMA) e multivariado (SARIMAX) utilizando métricas como MAE, RMSE e R².

**Resposta de Sucesso (200):**

- `data`: Dicionário contendo as métricas de avaliação para cada modelo.

### Observação

- **Endpoints de Comparação (`/compare_months`, `/compare_weeks`)**: Certifique-se de fornecer os parâmetros obrigatórios na query string da URL. Exemplo:

  ```
  http://localhost:5000/compare_months?month1=1&year1=2016&month2=2&year2=2016
  ```

## Considerações finais

Este projeto visa fornecer insights valiosos sobre o consumo energético, auxiliando usuários na tomada de decisões para otimização do uso de energia. Através da análise de dados históricos e da aplicação de modelos estatísticos avançados, é possível identificar padrões, prever consumos futuros e recomendar ações para a eficiência energética.

Sinta-se à vontade para contribuir com o projeto, reportar issues ou sugerir melhorias!