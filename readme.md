# PGAutoAPI

Uma api que trabalha automaticamente com as estuturas das tabelas 
no banco de dados.

## Funcionamento

Para cada tabela citada, esta api cria vários métodos de manipulação como:

* `GET /<table_name>/`  - Listagem e obtenção de registros
* `POST /<table_name>/` - Criação de registros novos
* `DELETE /<table_name>/?pk=x` - Exclusão de registros
* `PUT /<table_name>/` - Atualização de regisros

# Desenvolvimento

    pip install -r requirements.txt

## Executar com debug

    uvicorn main:app --reload

## Paths

Caminho comum da API

    http://localhost:8000/ 

Caminho da documentação

    http://localhost:8000/docs

