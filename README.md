<div align="center">

# Python Cloud Database

Aplicação Python que gera dados de crescimento bacteriano e os armazena em um
banco MySQL na Aiven.

[![Verificação do código Python](https://github.com/lianeheidemann/python_cloud_database/actions/workflows/python-checks.yml/badge.svg)](https://github.com/lianeheidemann/python_cloud_database/actions/workflows/python-checks.yml)

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.4-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Aiven](https://img.shields.io/badge/Aiven-Cloud-FF3554?style=for-the-badge&logo=aiven&logoColor=white)
![PyMySQL](https://img.shields.io/badge/PyMySQL-Driver-00618A?style=for-the-badge&logo=python&logoColor=white)

</div>

## Sobre

O projeto usa Python, PyMySQL e SSL para conectar-se ao MySQL na nuvem. A
aplicação cria a tabela automaticamente, limpa os registros anteriores, insere
os novos valores e consulta o resultado.

```text
Python → PyMySQL/SSL → Aiven MySQL
```

## Tecnologias

| Tecnologia | Finalidade |
| --- | --- |
| Python | Lógica da aplicação |
| PyMySQL | Driver de conexão com o MySQL |
| python-dotenv | Leitura das variáveis do `.env` |
| cryptography | Suporte à autenticação segura |
| MySQL | Armazenamento relacional |
| Aiven | Hospedagem gerenciada do banco |


## Pré-requisitos

- Python 3;
- Git;
- conta na Aiven com um serviço **MySQL Free** ativo;
- certificado CA fornecido pela Aiven;
- MySQL Workbench para consultas gráficas.

## Como executar

### 1. Clone o projeto

```powershell
git clone https://github.com/lianeheidemann/python_cloud_database.git
cd python_cloud_database
```

### 2. Crie o ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure a conexão

Crie um serviço MySQL na [Aiven](https://console.aiven.io/), baixe o certificado
CA e salve-o como `ca.pem` na raiz do projeto.

Copie `.env.example` para `.env`:

```powershell
Copy-Item .env.example .env
```

Preencha o arquivo:

```env
DB_HOST=host-da-aiven
DB_PORT=porta-da-aiven
DB_USER=usuario-da-aiven
DB_PASSWORD="senha-da-aiven"
DB_NAME=defaultdb
DB_SSL_CA=ca.pem
```

### 5. Execute

```powershell
python main.py
```

## Consultar os dados

Use uma conexão Aiven no MySQL Workbench:

```sql
SELECT *
FROM defaultdb.minhaTabela
ORDER BY id;
```

## Estrutura

```text
python_cloud_database/
├── docs/
│   └── configuracao_mysql.md
├── .env                          # credenciais locais, não versionado
├── .env.example                  # modelo das variáveis de ambiente
├── .gitignore                    # regras de exclusão do Git
├── ca.pem                        # certificado CA da Aiven
├── calculo.py                    # gera os valores armazenados
├── main.py                       # conexão e operações no MySQL
├── requirements.txt              # dependências com versões fixadas
└── README.md
```

As pastas `.venv/` e `__pycache__/` são geradas localmente e não são
versionadas.

> [!WARNING]
> Cada execução remove os registros anteriores com `TRUNCATE TABLE`.

Credenciais e Service URI nunca devem ser enviadas ao GitHub. Consulte o
[guia de configuração](docs/configuracao_mysql.md) para instruções detalhadas.
