import uuid

from main import conectar


def test_crud_completo_aiven():
    """Testa criação, inserção, consulta e exclusão na Aiven."""
    nome_tabela = f"github_actions_test_{uuid.uuid4().hex}"
    identificador = str(uuid.uuid4())
    valor_teste = "teste-crud-github-actions"

    conexao = conectar()

    try:
        with conexao.cursor() as cursor:
            # Cria uma tabela exclusiva para esta execução
            cursor.execute(
                f"""
                CREATE TABLE `{nome_tabela}` (
                    id CHAR(36) NOT NULL,
                    valor VARCHAR(100) NOT NULL,
                    PRIMARY KEY (id)
                )
                """
            )
            print(f"Tabela criada: {nome_tabela}")

            # Insere um registro
            cursor.execute(
                f"INSERT INTO `{nome_tabela}` (id, valor) VALUES (%s, %s)",
                (identificador, valor_teste),
            )
            conexao.commit()

            # Consulta e verifica o registro
            cursor.execute(
                f"SELECT valor FROM `{nome_tabela}` WHERE id = %s",
                (identificador,),
            )
            assert cursor.fetchone() == (valor_teste,)
            resultado = cursor.fetchone()
            print(f"Registro consultado: {resultado}")
            assert resultado == (valor_teste,)

            # Exclui o registro
            cursor.execute(
                f"DELETE FROM `{nome_tabela}` WHERE id = %s",
                (identificador,),
            )
            conexao.commit()

            # Confirma que foi excluído
            cursor.execute(
                f"SELECT COUNT(*) FROM `{nome_tabela}` WHERE id = %s",
                (identificador,),
            )
            assert cursor.fetchone()[0] == 0

    finally:
        # Remove somente a tabela temporária criada pelo teste
        with conexao.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS `{nome_tabela}`")
            conexao.commit()

        conexao.close()
