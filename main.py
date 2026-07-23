import os
from pathlib import Path

import pymysql
from calculo import calcula_bacterias
from dotenv import load_dotenv


load_dotenv()

# Configurações do banco de dados Aiven
BASE_DIR = Path(__file__).resolve().parent

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "defaultdb"),
    "charset": "utf8mb4",
    "connect_timeout": 10,
    "read_timeout": 10,
    "write_timeout": 10,
}


def obter_certificado_ssl():
    """Retorna o certificado SSL configurado ou interrompe a execução."""
    caminho_certificado = os.getenv("DB_SSL_CA")

    if not caminho_certificado:
        raise ValueError(
            "DB_SSL_CA é obrigatório para conectar com SSL à Aiven."
        )

    certificado = Path(caminho_certificado)

    if not certificado.is_absolute():
        certificado = BASE_DIR / certificado

    certificado = certificado.resolve()

    if not certificado.is_file():
        raise FileNotFoundError(
            f"Certificado SSL não encontrado: {certificado}"
        )

    return certificado


def conectar():
    """Cria uma conexão com SSL obrigatório e validação do servidor."""
    certificado = obter_certificado_ssl()
    configuracao = DB_CONFIG.copy()
    configuracao["ssl"] = {
        "ca": str(certificado),
        "check_hostname": True,
    }
    return pymysql.connect(**configuracao)


def migrar_coluna_populacao(cursor):
    """Renomeia a coluna legada sem perder os dados existentes."""
    cursor.execute(
        """
        SELECT COLUMN_NAME
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = DATABASE()
          AND TABLE_NAME = 'crescimento_bacteriano'
          AND COLUMN_NAME IN ('populacaoperiodo', 'populacao_periodo')
        """
    )
    colunas = {linha[0] for linha in cursor.fetchall()}

    if "populacaoperiodo" in colunas and "populacao_periodo" in colunas:
        raise RuntimeError(
            "As colunas populacaoperiodo e populacao_periodo coexistem. "
            "Revise a estrutura antes de continuar."
        )

    if "populacaoperiodo" in colunas:
        cursor.execute(
            """
            ALTER TABLE crescimento_bacteriano
            RENAME COLUMN populacaoperiodo TO populacao_periodo
            """
        )
        print("Coluna populacaoperiodo migrada para populacao_periodo.")


def criar_tabelas():
    """Cria as tabelas e aplica migrações compatíveis, caso necessário."""
    sql_simulacoes = """
        CREATE TABLE IF NOT EXISTS simulacoes_bacterianas (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
            data_simulacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            populacao_inicial BIGINT UNSIGNED NOT NULL,
            quantidade_periodos INT UNSIGNED NOT NULL,
            PRIMARY KEY (id)
        )
    """

    sql_crescimento = """
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
        )
    """

    conexao = conectar()

    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql_simulacoes)
            cursor.execute(sql_crescimento)
            migrar_coluna_populacao(cursor)

        conexao.commit()
        print("Tabelas verificadas com sucesso!")

    except (pymysql.MySQLError, RuntimeError):
        conexao.rollback()
        raise

    finally:
        conexao.close()


def registrar_simulacao(populacao_inicial, quantidade_periodos, populacoes):
    """Registra uma simulação e os valores calculados para cada período."""
    if len(populacoes) != quantidade_periodos:
        raise ValueError(
            "A quantidade de valores deve corresponder à quantidade de períodos."
        )

    sql_simulacao = """
        INSERT INTO simulacoes_bacterianas (
            populacao_inicial,
            quantidade_periodos
        )
        VALUES (%s, %s)
    """

    sql_periodos = """
        INSERT INTO crescimento_bacteriano (
            simulacao_id,
            periodo,
            populacao_periodo
        )
        VALUES (%s, %s, %s)
    """

    conexao = conectar()

    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                sql_simulacao,
                (populacao_inicial, quantidade_periodos),
            )
            simulacao_id = cursor.lastrowid

            registros = [
                (simulacao_id, periodo, populacao)
                for periodo, populacao in enumerate(populacoes, start=1)
            ]
            cursor.executemany(sql_periodos, registros)

        conexao.commit()
        print(f"Simulação {simulacao_id} registrada com sucesso!")
        return simulacao_id

    except pymysql.MySQLError:
        conexao.rollback()
        raise

    finally:
        conexao.close()


def mostrar_dados(simulacao_id):
    """Mostra os dados e os resultados de uma simulação."""
    sql = """
        SELECT
            s.id,
            s.data_simulacao,
            s.populacao_inicial,
            s.quantidade_periodos,
            c.periodo,
            c.populacao_periodo
        FROM simulacoes_bacterianas AS s
        INNER JOIN crescimento_bacteriano AS c
            ON c.simulacao_id = s.id
        WHERE s.id = %s
        ORDER BY c.periodo
    """

    conexao = conectar()

    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (simulacao_id,))
            resultados = cursor.fetchall()

        if not resultados:
            print(f"Nenhum resultado encontrado para a simulação {simulacao_id}.")
            return

        primeiro = resultados[0]
        print(f"\nSimulação: {primeiro[0]}")
        print(f"Data: {primeiro[1]}")
        print(f"População inicial: {primeiro[2]}")
        print(f"Quantidade de períodos: {primeiro[3]}")
        print("\nResultados:")

        for resultado in resultados:
            print(f"Período {resultado[4]}: {resultado[5]}")

    finally:
        conexao.close()


if __name__ == "__main__":
    populacao_inicial = 5
    quantidade_periodos = 10

    populacoes = calcula_bacterias(
        populacao_inicial,
        quantidade_periodos,
    )

    print("\nLista gerada:")
    print(populacoes)
    print(f"\nTamanho da lista: {len(populacoes)}")

    criar_tabelas()
    nova_simulacao_id = registrar_simulacao(
        populacao_inicial,
        quantidade_periodos,
        populacoes,
    )
    mostrar_dados(nova_simulacao_id)
