# Configuração do MySQL para o projeto

Este guia mostra o que deve ser feito no **MySQL Workbench** antes de executar o arquivo `main.py`.

## 1. Abra o MySQL Workbench

1. Inicie o **MySQL Workbench**.
2. Abra a conexão local do MySQL.
3. Informe a senha do usuário configurado durante a instalação.

Normalmente, o usuário local é:

```text
root
```

## 2. Crie o banco de dados

Abra uma nova aba de consulta no MySQL Workbench e execute:

```sql
CREATE DATABASE IF NOT EXISTS python_cloud_database
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Esse comando cria o banco de dados utilizado pelo projeto.

## 3. Selecione o banco

Execute:

```sql
USE python_cloud_database;
```

A partir desse momento, os próximos comandos serão executados dentro desse banco.

## 4. Crie a tabela

Execute:

```sql
CREATE TABLE IF NOT EXISTS minhaTabela (
    valores BIGINT NOT NULL
);
```

A tabela precisa se chamar exatamente `minhaTabela`, porque esse é o nome utilizado no código Python.

A coluna `valores` armazena os números gerados pelo programa.

## 5. Verifique se tudo foi criado

Execute:

```sql
SHOW DATABASES;
```

Depois:

```sql
USE python_cloud_database;

SHOW TABLES;
```

Para verificar a estrutura da tabela:

```sql
DESCRIBE minhaTabela;
```

O resultado deve mostrar uma coluna chamada `valores`, do tipo `BIGINT`.

## 6. Configure o arquivo `.env`

Na pasta do projeto, crie um arquivo chamado `.env` com os dados da sua conexão local:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_do_mysql
DB_NAME=python_cloud_database
```

Substitua `sua_senha_do_mysql` pela senha usada para entrar no MySQL Workbench.

Não envie o arquivo `.env` para o GitHub.

## 7. Execute o programa

No terminal do VS Code, execute:

```bash
python main.py
```

O programa irá:

1. gerar uma lista de valores;
2. apagar os registros antigos da tabela;
3. inserir os novos valores;
4. consultar os dados;
5. mostrar os resultados no terminal.

Não é necessário inserir os dados manualmente no MySQL Workbench.

## 8. Consultar os dados manualmente

Para ver os registros salvos, execute no MySQL Workbench:

```sql
USE python_cloud_database;

SELECT * FROM minhaTabela;
```

## 9. Apagar os registros manualmente

Para limpar todos os registros da tabela:

```sql
TRUNCATE TABLE minhaTabela;
```

Esse comando mantém a tabela, mas remove todos os dados armazenados.

## Script completo

Você também pode executar todos os comandos de configuração de uma vez:

```sql
CREATE DATABASE IF NOT EXISTS python_cloud_database
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE python_cloud_database;

CREATE TABLE IF NOT EXISTS minhaTabela (
    valores BIGINT NOT NULL
);

SHOW TABLES;

DESCRIBE minhaTabela;
```

## Possíveis erros

### Erro: acesso negado

Mensagem semelhante:

```text
Access denied for user
```

Verifique o usuário e a senha informados no arquivo `.env`.

### Erro: banco de dados desconhecido

Mensagem semelhante:

```text
Unknown database 'python_cloud_database'
```

Execute novamente o comando de criação do banco.

### Erro: tabela não encontrada

Mensagem semelhante:

```text
Table 'python_cloud_database.minhaTabela' doesn't exist
```

Selecione o banco e crie a tabela:

```sql
USE python_cloud_database;

CREATE TABLE minhaTabela (
    valores BIGINT NOT NULL
);
```

### Erro: não foi possível conectar ao MySQL

Verifique se o serviço do MySQL está em execução no Windows.

O serviço geralmente aparece com o nome:

```text
MySQL80
```
