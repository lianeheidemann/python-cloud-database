from main import conectar


def test_conexao_aiven():
    """Verifica a conexão SSL com a Aiven sem alterar dados."""
    conexao = conectar()

    try:
        with conexao.cursor() as cursor:
            cursor.execute("SELECT 1")
            resultado = cursor.fetchone()

        assert resultado == (1,)

    finally:
        conexao.close()
