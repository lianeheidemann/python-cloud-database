# Sistema de Armazenamento de Dados com Python e MySQL
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white"/> <img src="https://img.shields.io/badge/PyMySQL-3776AB?style=for-the-badge&logo=python&logoColor=white"/>

Projeto desenvolvido em Python para realizar operações de **armazenamento, leitura e limpeza de dados** em um banco de dados MySQL hospedado online.

---

## Como executar o projeto

### Pré-requisitos

Antes de iniciar, instale:

* Python 3
* MySQL Server
* MySQL Workbench
* Visual Studio Code

### 1. Clone o repositório

```bash
git clone https://github.com/lianeheidemann/python_cloud_database.git
cd python_cloud_database
```

### 2. Crie o ambiente virtual

No terminal do VS Code:

```bash
python -m venv .venv
```

No Windows, ative com:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
pip install pymysql python-dotenv
```

### 4. Configure o banco de dados

No MySQL Workbench, execute:

```sql
CREATE DATABASE python_cloud_database;

USE python_cloud_database;

CREATE TABLE minhaTabela (
    valores BIGINT NOT NULL
);
```

### 5. Configure as variáveis de ambiente

Crie uma cópia do arquivo `.env.example` com o nome `.env`:

```powershell
Copy-Item .env.example .env
```

Preencha o arquivo com os dados do seu MySQL local:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=python_cloud_database
```

> O arquivo `.env` contém informações sensíveis e não deve ser enviado para o GitHub.

### 6. Execute o projeto

```bash
python main.py
```

O programa irá:

* gerar uma lista de valores;
* limpar os registros existentes;
* inserir os novos dados no MySQL;
* consultar e exibir os registros no terminal.

### Estrutura esperada

```text
python_cloud_database/
├── .env
├── .env.example
├── .gitignore
├── calculo.py
├── main.py
└── README.md
```

> O arquivo `calculo.py` deve conter a função `calcula_bacterias`, utilizada pelo arquivo `main.py`.

