# Utilizando o Servidor: db4free.net
import os
import pymysql
from calculo import calcula_bacterias
from dotenv import load_dotenv


load_dotenv()

# Configurações do banco de dados
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}


def conectar():
    """
    Cria e retorna uma conexão com o banco de dados.
    """
    return pymysql.connect(**DB_CONFIG)


def inserir_dados(valor):
    """
    Insere um valor na tabela.
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

    except pymysql.MySQLError as erro:
        conexao.rollback()
        print(f"Erro ao inserir dados: {erro}")

    finally:
        cursor.close()
        conexao.close()


def mostrar_dados():
    """
    Mostra todos os dados da tabela.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "SELECT * FROM minhaTabela"

    try:
        cursor.execute(sql)
        resultados = cursor.fetchall()

        print("\nDados da tabela:\n")

        for row in resultados:
            print(f"Valor: {row[0]}")

    except pymysql.MySQLError as erro:
        print(f"Erro ao buscar dados: {erro}")

    finally:
        cursor.close()
        conexao.close()


def limpar_tabela():
    """
    Limpa todos os dados da tabela.
    """
    conexao = conectar()
    cursor = conexao.cursor()

    sql = "TRUNCATE TABLE minhaTabela"

    try:
        cursor.execute(sql)
        conexao.commit()
        print("Tabela limpa com sucesso!")

    except pymysql.MySQLError as erro:
        conexao.rollback()
        print(f"Erro ao limpar tabela: {erro}")

    finally:
        cursor.close()
        conexao.close()


def inserir_lista(lista):
    """
    Insere todos os valores da lista no banco.
    """
    for valor in lista:
        print(f"Inserindo: {valor}")
        inserir_dados(valor)


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

    # Limpa tabela antes de inserir novos dados
    limpar_tabela()

    # Insere os dados no banco
    inserir_lista(lista)

    # Mostra os dados inseridos
    mostrar_dados()
