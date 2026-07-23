<div align="center">

# Python Cloud Database

Aplicação Python que simula o crescimento de uma população bacteriana e
armazena os resultados em um banco MySQL gerenciado na Aiven.

[![Verificação do código Python](https://github.com/lianeheidemann/python_cloud_database/actions/workflows/python-checks.yml/badge.svg)](https://github.com/lianeheidemann/python_cloud_database/actions/workflows/python-checks.yml)
[![Teste de conexão Aiven](https://github.com/lianeheidemann/python_cloud_database/actions/workflows/aiven-connection.yml/badge.svg?event=workflow_dispatch)](https://github.com/lianeheidemann/python_cloud_database/actions/workflows/aiven-connection.yml)

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.4-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Aiven](https://img.shields.io/badge/Aiven-Cloud-FF3554?style=for-the-badge&logo=aiven&logoColor=white)
![PyMySQL](https://img.shields.io/badge/PyMySQL-Driver-00618A?style=for-the-badge&logo=python&logoColor=white)

</div>

## Visão geral

O projeto demonstra um fluxo completo de integração entre Python e um banco
MySQL em nuvem. A aplicação:

1. calcula uma sequência de crescimento bacteriano;
2. estabelece uma conexão SSL com a Aiven;
3. cria as tabelas `simulacoes_bacterianas` e `crescimento_bacteriano`;
4. registra a data, a população inicial e a quantidade de períodos;
5. insere os resultados de cada período em uma única transação;
6. consulta a simulação recém-registrada sem apagar o histórico.

```mermaid
flowchart LR
    A["calculo.py"] --> B["main.py"]
    B --> C["PyMySQL + SSL"]
    C --> D["Aiven MySQL"]
```

Com a configuração padrão, a população começa em `5` e dobra durante dez
períodos:

```text
[5, 10, 20, 40, 80, 160, 320, 640, 1280, 2560]
```

## Funcionalidades

- geração determinística dos dados de crescimento;
- validação de população inicial e quantidade de períodos;
- configuração por variáveis de ambiente;
- conexão MySQL com SSL obrigatório e validação da existência do certificado CA;
- criação automática das tabelas e de suas chaves primária e estrangeira;
- histórico separado de cada simulação;
- inserção parametrizada dos períodos em uma única transação;
- consulta ordenada dos resultados de cada simulação;
- rollback em falhas de escrita;
- teste real de conexão com `SELECT 1`;
- teste real das tabelas, da chave estrangeira, do histórico e do `ON DELETE CASCADE` na Aiven;
- limpeza automática dos recursos temporários criados pelos testes;
- verificação automática de sintaxe com GitHub Actions.

## Tecnologias

| Tecnologia | Finalidade |
| --- | --- |
| Python 3.13 | Lógica da aplicação e dos testes |
| MySQL 8.4 | Armazenamento relacional |
| Aiven | Hospedagem gerenciada do MySQL |
| PyMySQL | Driver de conexão com o banco |
| python-dotenv | Leitura das variáveis do arquivo `.env` |
| cryptography | Suporte à autenticação segura do driver |
| pytest | Testes automatizados |
| GitHub Actions | Integração contínua e testes manuais na nuvem |

## Modelo de dados

Cada execução gera um registro em `simulacoes_bacterianas`. Os resultados de
cada período ficam em `crescimento_bacteriano` e são associados à simulação
pela chave estrangeira `simulacao_id`.

```mermaid
erDiagram
    simulacoes_bacterianas ||--|{ crescimento_bacteriano : possui
    simulacoes_bacterianas {
        BIGINT id PK
        TIMESTAMP data_simulacao
        BIGINT populacao_inicial
        INT quantidade_periodos
    }
    crescimento_bacteriano {
        BIGINT id PK
        BIGINT simulacao_id FK
        INT periodo
        BIGINT populacao_periodo
    }
```

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


### Migração da coluna anterior

Ao iniciar, a aplicação consulta `information_schema.COLUMNS`. Se encontrar a
coluna legada `populacaoperiodo`, executa automaticamente:

```sql
ALTER TABLE crescimento_bacteriano
RENAME COLUMN populacaoperiodo TO populacao_periodo;
```

A operação preserva os registros existentes. Se os dois nomes forem encontrados
simultaneamente, a aplicação interrompe a execução para evitar uma migração
ambígua.

## Estrutura do projeto

```text
python_cloud_database/
├── .github/
│   └── workflows/
│       ├── aiven-connection.yml      # testes reais e manuais na Aiven
│       └── python-checks.yml         # verificação automática de sintaxe
├── docs/
│   └── configuracao_mysql.md         # configuração da Aiven e do Workbench
├── tests/
│   ├── test_aiven_connection.py      # teste SSL com SELECT 1
│   └── test_aiven_crud.py            # teste de integração do modelo real
├── .env.example                      # modelo das variáveis de ambiente
├── .gitignore                        # arquivos ignorados pelo Git
├── ca.pem                            # certificado CA da Aiven
├── calculo.py                        # cálculo do crescimento bacteriano
├── main.py                           # conexão e operações no MySQL
├── requirements.txt                   # dependências com versões fixadas
├── README.md                         # documentação atual
└── readme_v2.md                      # documentação ampliada
```

## Pré-requisitos

- Python 3.13 ou versão compatível;
- Git;
- serviço MySQL ativo na Aiven;
- certificado CA fornecido pela Aiven;
- MySQL Workbench, opcionalmente, para consultas gráficas.

Não é necessário instalar ou executar um servidor MySQL local.

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/lianeheidemann/python_cloud_database.git
cd python_cloud_database
```

### 2. Crie o ambiente virtual

```bash
python -m venv .venv
```

Ative o ambiente no Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Configuração da Aiven

No painel da Aiven, abra o serviço MySQL e copie os dados apresentados em
**Connection information**. Baixe também o **CA Certificate**.

Crie o arquivo `.env` a partir do modelo:

```powershell
Copy-Item .env.example .env
```

No Linux ou macOS:

```bash
cp .env.example .env
```

Preencha o `.env`:

```env
DB_HOST=host-fornecido-pela-aiven
DB_PORT=porta-fornecida-pela-aiven
DB_USER=usuario-fornecido-pela-aiven
DB_PASSWORD="senha-fornecida-pela-aiven"
DB_NAME=defaultdb
DB_SSL_CA=ca.pem
```

Salve o certificado da Aiven como `ca.pem` na raiz do projeto. A variável
`DB_SSL_CA` é obrigatória: se estiver ausente ou apontar para um arquivo
inexistente, o programa interromperá a execução antes de tentar a conexão.
Consulte o [guia detalhado de configuração](docs/configuracao_mysql.md) para
configurar também o MySQL Workbench.

## Execução

Com o ambiente virtual ativo e o `.env` configurado:

```bash
python main.py
```

Saída resumida:

```text
Lista gerada:
[5, 10, 20, 40, 80, 160, 320, 640, 1280, 2560]

Tamanho da lista: 10
Tabelas verificadas com sucesso!
Simulação 1 registrada com sucesso!
```

Para consultar os registros no MySQL Workbench:

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

## Testes

### Testes locais

Os testes usam uma conexão real com a Aiven. Configure o `.env` e execute:

```bash
python -m pytest -q -s tests
```

O primeiro teste valida a conexão SSL com `SELECT 1`. O segundo valida o modelo
relacional usado pela aplicação:

- confirma a existência de `simulacoes_bacterianas` e `crescimento_bacteriano`;
- registra duas simulações diferentes;
- comprova que o histórico da primeira permanece após o segundo registro;
- verifica a chave estrangeira;
- verifica o `ON DELETE CASCADE`;
- confirma que excluir uma simulação não afeta a outra.

Saída resumida esperada:

```text
Tabelas verificadas com sucesso!
Simulação ... registrada com sucesso!
Simulação ... registrada com sucesso!
4 passed
```

O teste insere temporariamente duas simulações no modelo real e remove, no bloco
`finally`, somente os registros criados por sua própria execução. A exclusão
dos períodos relacionados ocorre pela regra `ON DELETE CASCADE`.

### GitHub Actions

| Workflow | Acionamento | Verificação |
| --- | --- | --- |
| `python-checks.yml` | Push, pull request ou execução manual | Compila `main.py` e `calculo.py` para detectar erros de sintaxe |
| `aiven-connection.yml` | Todo push ou execução manual | Testa a conexão e a integridade do modelo relacional na Aiven |

Para executar o teste da Aiven:

1. abra a aba **Actions**;
2. selecione **Teste de conexão Aiven**;
3. clique em **Run workflow**;
4. escolha a branch que deseja testar;
5. confirme a execução.

O workflow utiliza estes **Repository Secrets**:

| Secret | Conteúdo esperado |
| --- | --- |
| `AIVEN_DB_HOST` | Host do serviço |
| `AIVEN_DB_PORT` | Porta do serviço |
| `AIVEN_DB_USER` | Usuário do banco |
| `AIVEN_DB_PASSWORD` | Senha do banco |
| `AIVEN_DB_NAME` | Nome do banco, normalmente `defaultdb` |

O caminho `DB_SSL_CA: ca.pem` é definido no YAML porque identifica um arquivo,
não uma credencial secreta.

## Segurança

- nunca publique o `.env`, a senha ou a Service URI;
- mantenha somente valores ilustrativos no `.env.example`;
- armazene credenciais de automação em GitHub Secrets;
- utilize o certificado CA para validar a identidade do servidor;
- altere imediatamente qualquer credencial exposta;
- não grave senhas diretamente no código ou no workflow.

> [!NOTE]
> Cada execução de `main.py` cria uma nova simulação. Os registros das
> simulações anteriores são preservados.

## Solução de problemas

O guia [Configuração do MySQL na Aiven](docs/configuracao_mysql.md) reúne
instruções para:

- configurar SSL;
- conectar pelo MySQL Workbench;
- corrigir `Access denied`;
- identificar uma conexão acidental com o MySQL local;
- resolver erros relacionados ao certificado ou à chave primária.

## Melhorias futuras

- criar testes unitários para `calculo.py`;
- validar as variáveis de ambiente antes da conexão;
- substituir os `print()` por logs estruturados;
- adicionar relatório de cobertura de testes.

