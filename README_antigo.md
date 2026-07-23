<div align="center">

# Python Cloud Database

Aplicação Python para geração e persistência de dados de crescimento bacteriano
em um banco MySQL gerenciado na Aiven.

![Python](https://img.shields.io/badge/Python-3-3776AB?style=flat-square&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Aiven](https://img.shields.io/badge/Cloud-Aiven-FF3554?style=flat-square)
![PyMySQL](https://img.shields.io/badge/Driver-PyMySQL-3776AB?style=flat-square)

</div>

## Visão geral

O projeto demonstra um fluxo completo de integração entre Python e MySQL em
nuvem. A aplicação calcula uma sequência simples de crescimento bacteriano,
estabelece uma conexão SSL com a Aiven e armazena os resultados em uma tabela
relacional.

```text
calculo.py → main.py → PyMySQL/SSL → Aiven MySQL → defaultdb.minhaTabela
```

A sequência começa com uma população de `5` bactérias e dobra a cada período:

```text
[5, 10, 20, 40, 80, 160, 320, 640, 1280, 2560]
```

## Recursos

- geração determinística de dados de crescimento bacteriano;
- configuração por variáveis de ambiente;
- conexão MySQL protegida por SSL e certificado CA;
- criação automática da tabela e de sua chave primária;
- limpeza, inserção e consulta dos registros;
- compatibilidade com MySQL Workbench;
- credenciais separadas do código-fonte.

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
- MySQL Workbench opcional para consultas gráficas.

Não é necessário executar um servidor MySQL localmente.

## Início rápido

### 1. Clone o repositório

```powershell
git clone https://github.com/lianeheidemann/python_cloud_database.git
cd python_cloud_database
```

### 2. Crie e ative o ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

O terminal exibirá `(.venv)` enquanto o ambiente estiver ativo.

### 3. Instale as dependências

```powershell
python -m pip install pymysql python-dotenv cryptography
```

### 4. Configure o banco

Crie um serviço MySQL no [Aiven Console](https://console.aiven.io/) e aguarde
até que o status seja **Running**.

O passo a passo completo está em
[CONFIGURACAO_MYSQL.md](assets/CONFIGURACAO_MYSQL.md).

### 5. Configure as variáveis de ambiente

Crie o `.env` a partir do modelo:

```powershell
Copy-Item .env.example .env
```

Preencha com os dados apresentados em **Connection information** na Aiven:

```env
DB_HOST=host-fornecido-pela-aiven
DB_PORT=porta-fornecida-pela-aiven
DB_USER=usuario-fornecido-pela-aiven
DB_PASSWORD="senha-fornecida-pela-aiven"
DB_NAME=defaultdb
DB_SSL_CA=ca.pem
```

Baixe o **CA Certificate** da Aiven e salve-o como `ca.pem` na raiz do
projeto.

### 6. Execute

```powershell
python main.py
```

Saída resumida:

```text
Lista gerada:
[5, 10, 20, 40, 80, 160, 320, 640, 1280, 2560]

Tamanho da lista: 10
Tabela verificada com sucesso!
Tabela limpa com sucesso!
```

## Modelo de dados

A tabela é criada automaticamente:

```sql
CREATE TABLE IF NOT EXISTS minhaTabela (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    valores BIGINT NOT NULL,
    PRIMARY KEY (id)
);
```

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| `id` | `BIGINT UNSIGNED` | Identificador único e auto-incrementável |
| `valores` | `BIGINT` | População calculada em cada período |

Para consultar os registros:

```sql
SELECT *
FROM defaultdb.minhaTabela
ORDER BY id;
```

## Arquitetura do projeto

```text
python_cloud_database/
├── .env.example              # modelo das variáveis de ambiente
├── .gitignore                # arquivos excluídos do versionamento
├── ca.pem                    # certificado CA da Aiven
├── calculo.py                # cálculo do crescimento bacteriano
├── assets/
│   └── CONFIGURACAO_MYSQL.md # guia de configuração da Aiven e Workbench
├── main.py                   # conexão e operações no banco
└── README.md                 # documentação principal
```

Arquivos locais como `.env`, `.venv/` e `__pycache__/` não devem ser
versionados.

## MySQL Workbench

Crie uma conexão chamada `Aiven MySQL` usando o Host, Port, User e Password
fornecidos pela Aiven. Na aba **SSL**, selecione **Require and Verify CA** e
informe o caminho completo do arquivo `ca.pem`.

> A conexão `Local instance MySQL80` representa o servidor instalado no
> computador e não exibe os dados armazenados na Aiven.

## Segurança

- nunca publique o `.env`, a senha ou a Service URI;
- mantenha somente valores ilustrativos no `.env.example`;
- utilize o certificado CA para validar a identidade do servidor;
- altere imediatamente qualquer credencial exposta;
- não armazene senhas diretamente no código Python.

> [!WARNING]
> Cada execução chama `TRUNCATE TABLE` e remove os registros anteriores antes
> de inserir a nova sequência. Comente ou remova `limpar_tabela()` caso seja
> necessário preservar os dados existentes.

## Documentação adicional

Consulte [CONFIGURACAO_MYSQL.md](assets/CONFIGURACAO_MYSQL.md) para instruções de
criação do serviço, configuração SSL, conexão pelo Workbench e solução de
problemas comuns.
