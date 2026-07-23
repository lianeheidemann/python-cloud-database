# Configuração do MySQL na Aiven

Este guia explica como criar e acessar o banco MySQL em nuvem usado pelo projeto.

## 1. Criar o serviço

1. Acesse [Aiven Console](https://console.aiven.io/).
2. Entre no projeto desejado.
3. Selecione **Services > Create service**.
4. Escolha **MySQL**. Não escolha Apache Kafka.
5. Selecione o plano **Free**.
6. Aguarde o serviço ficar com o status **Running**.

## 2. Obter os dados da conexão

Na página **Overview** do serviço MySQL, localize **Connection information**.
Copie os valores de:

- Host
- Port
- User
- Password
- Database

Não publique a senha nem a Service URI.

## 3. Baixar o certificado

Na mesma página, baixe o **CA Certificate** e salve o arquivo como `ca.pem`
na raiz do projeto:

```text
python_cloud_database/
├── ca.pem
├── calculo.py
├── main.py
└── README.md
```

## 4. Configurar o `.env`

Copie `.env.example` para `.env`:

```powershell
Copy-Item .env.example .env
```

Preencha o `.env` com os valores fornecidos pela Aiven:

```env
DB_HOST=host-fornecido-pela-aiven
DB_PORT=porta-fornecida-pela-aiven
DB_USER=usuario-fornecido-pela-aiven
DB_PASSWORD="senha-fornecida-pela-aiven"
DB_NAME=defaultdb
DB_SSL_CA=ca.pem
```

Use no `DB_NAME` exatamente o valor exibido no campo **Database** da Aiven.
O nome inicial normalmente é `defaultdb`.

`DB_SSL_CA` é obrigatório. A aplicação interrompe a execução se essa variável
não estiver definida ou se o caminho não apontar para um arquivo existente.

## 5. Executar o programa

Ative o ambiente virtual e execute:

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

O programa:

1. conecta ao MySQL da Aiven usando SSL;
2. cria `simulacoes_bacterianas` e `crescimento_bacteriano`, se necessário;
3. registra a data, a população inicial e a quantidade de períodos;
4. insere os resultados vinculados à nova simulação;
5. consulta e mostra somente a simulação recém-registrada.

As tabelas possuem a seguinte estrutura:

```sql
CREATE TABLE IF NOT EXISTS simulacoes_bacterianas (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    data_simulacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    populacao_inicial BIGINT UNSIGNED NOT NULL,
    quantidade_periodos INT UNSIGNED NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS crescimento_bacteriano (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    simulacao_id BIGINT UNSIGNED NOT NULL,
    periodo INT UNSIGNED NOT NULL,
    populacao_periodo BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_simulacao_periodo (simulacao_id, periodo),
    CONSTRAINT fk_crescimento_simulacao
        FOREIGN KEY (simulacao_id)
        REFERENCES simulacoes_bacterianas (id)
        ON DELETE CASCADE
);
```

Se a tabela tiver sido criada pela versão anterior, a aplicação renomeará
automaticamente `populacaoperiodo` para `populacao_periodo`, preservando os
dados existentes.

## 6. Configurar o MySQL Workbench

Crie uma nova conexão com:

```text
Connection Name: Aiven MySQL
Connection Method: Standard (TCP/IP)
Hostname: valor de Host da Aiven
Port: valor de Port da Aiven
Username: valor de User da Aiven
Default Schema: defaultdb
```

Em **Password**, use **Store in Vault** e informe a senha sem aspas.

Na aba **SSL**, configure:

```text
SSL Mode: Require and Verify CA
SSL CA File: caminho completo para ca.pem
```

Teste e abra a conexão. Não use a conexão **Local instance MySQL80**, pois ela
aponta para o MySQL instalado no computador, não para a Aiven.

## 7. Consultar os dados

No MySQL Workbench conectado à Aiven, execute:

```sql
SELECT
    s.id AS simulacao,
    s.data_simulacao,
    s.populacao_inicial,
    s.quantidade_periodos,
    c.periodo,
    c.populacao_periodo
FROM defaultdb.simulacoes_bacterianas AS s
INNER JOIN defaultdb.crescimento_bacteriano AS c
    ON c.simulacao_id = s.id
ORDER BY s.id DESC, c.periodo;
```

## Problemas comuns

### Unknown database `defaultdb`

O Workbench provavelmente está conectado ao MySQL local. Abra a conexão
**Aiven MySQL**.

### Access denied

Confira usuário e senha. No Workbench, a senha deve ser informada sem aspas.
No `.env`, aspas são aceitas e recomendadas quando a senha contém caracteres
especiais.

### Incompatible/nonstandard server version

A Aiven pode usar MySQL 8.4, enquanto versões antigas do Workbench foram
testadas até MySQL 8.0. Para consultas comuns, selecione **Continue Anyway**.

### Erro de chave primária

A Aiven exige chave primária nas tabelas. O projeto já cria a coluna `id` como
chave primária; use a versão atual de `main.py`.

### Certificado não encontrado ou DB_SSL_CA ausente

A conexão SSL é obrigatória. Confirme que `ca.pem` está na raiz do projeto e que o `.env` contém:

```env
DB_SSL_CA=ca.pem
```

## Segurança

- Nunca envie `.env`, senha ou Service URI ao GitHub.
- O arquivo `.env.example` deve conter apenas valores ilustrativos.
- Troque imediatamente qualquer senha publicada acidentalmente.
- O certificado `ca.pem` é usado para validar a conexão SSL e não contém a
  senha do banco.
