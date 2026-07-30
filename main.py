import os
import sys
from pathlib import Path

import pymysql
from calculo import calcula_bacterias
from dotenv import load_dotenv


load_dotenv()

# Configurações do banco de dados Aiven
BASE_DIR = Path(__file__).resolve().parent
SSL_CA = os.getenv("DB_SSL_CA")

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

if SSL_CA:
    certificado = Path(SSL_CA)

    if not certificado.is_absolute():
        certificado = BASE_DIR / certificado

    DB_CONFIG["ssl"] = {
        "ca": str(certificado),
        "check_hostname": True,
    }


def conectar():
    """
    Cria e retorna uma conexão com o banco de dados.
    """
    return pymysql.connect(**DB_CONFIG)


def criar_tabela():
    """
    Cria a tabela caso ela ainda não exista.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        CREATE TABLE IF NOT EXISTS minhaTabela (
            id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
            valores BIGINT NOT NULL,
            PRIMARY KEY (id)
        )
    """

    try:
        cursor.execute(sql)
        conexao.commit()
        print("Tabela verificada com sucesso!")

    finally:
        cursor.close()
        conexao.close()


def inserir_dados(valor):
    """
    Insere um valor na tabela. Retorna True em caso de sucesso, False em falha.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO minhaTabela(valores)
        VALUES (%s)
    """

    try:
        cursor.execute(sql, (valor,))
        conexao.commit()
        print(f"Valor {valor} inserido com sucesso!")
        return True

    except pymysql.MySQLError as erro:
        conexao.rollback()
        print(f"Erro ao inserir dados: {erro}")
        return False

    finally:
        cursor.close()
        conexao.close()


def mostrar_dados():
    """
    Mostra todos os dados da tabela. Retorna True em caso de sucesso, False em falha.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT valores FROM minhaTabela ORDER BY id"

    try:
        cursor.execute(sql)
        resultados = cursor.fetchall()

        print("\nDados da tabela:\n")

        for row in resultados:
            print(f"Valor: {row[0]}")

        return True

    except pymysql.MySQLError as erro:
        print(f"Erro ao buscar dados: {erro}")
        return False

    finally:
        cursor.close()
        conexao.close()


def limpar_tabela():
    """
    Limpa todos os dados da tabela. Retorna True em caso de sucesso, False em falha.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "TRUNCATE TABLE minhaTabela"

    try:
        cursor.execute(sql)
        conexao.commit()
        print("Tabela limpa com sucesso!")
        return True

    except pymysql.MySQLError as erro:
        conexao.rollback()
        print(f"Erro ao limpar tabela: {erro}")
        return False

    finally:
        cursor.close()
        conexao.close()


def inserir_lista(lista):
    """
    Insere todos os valores da lista no banco.
    Retorna True se todos os inserts tiverem sucesso, False caso algum falhe.
    """
    sucesso = True

    for valor in lista:
        print(f"Inserindo: {valor}")
        if not inserir_dados(valor):
            sucesso = False

    return sucesso


def tamanho_lista(lista):
    """
    Retorna o tamanho da lista.
    """
    return len(lista)


if __name__ == "__main__":

    # Gera a lista de bactérias
    lista = calcula_bacterias(5)

    print("\nLista gerada:")
    print(lista)

    print(f"\nTamanho da lista: {tamanho_lista(lista)}")

    # Cria a tabela e limpa os registros antes de inserir novos dados
    criar_tabela()

    sucesso = limpar_tabela()

    # Insere os dados no banco
    sucesso = inserir_lista(lista) and sucesso

    # Mostra os dados inseridos
    sucesso = mostrar_dados() and sucesso

    if not sucesso:
        sys.exit(1)
