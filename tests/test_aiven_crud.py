import pymysql
import pytest

from main import conectar, criar_tabelas, registrar_simulacao


def test_modelo_relacional_aiven():
    """Valida o modelo real, o histórico, a chave estrangeira e o cascade."""
    simulacao_ids = []
    criar_tabelas()

    try:
        primeira_populacao = 3
        primeira_sequencia = [3, 6, 12]
        primeira_id = registrar_simulacao(
            primeira_populacao,
            len(primeira_sequencia),
            primeira_sequencia,
        )
        simulacao_ids.append(primeira_id)

        segunda_populacao = 11
        segunda_sequencia = [11, 22]
        segunda_id = registrar_simulacao(
            segunda_populacao,
            len(segunda_sequencia),
            segunda_sequencia,
        )
        simulacao_ids.append(segunda_id)

        conexao = conectar()

        try:
            with conexao.cursor() as cursor:
                # Confirma que as duas tabelas do modelo existem
                cursor.execute(
                    """
                    SELECT TABLE_NAME
                    FROM information_schema.TABLES
                    WHERE TABLE_SCHEMA = DATABASE()
                      AND TABLE_NAME IN (
                          'simulacoes_bacterianas',
                          'crescimento_bacteriano'
                      )
                    """
                )
                tabelas = {linha[0] for linha in cursor.fetchall()}
                assert tabelas == {
                    "simulacoes_bacterianas",
                    "crescimento_bacteriano",
                }

                # Confirma a chave estrangeira e sua regra de exclusão
                cursor.execute(
                    """
                    SELECT DELETE_RULE
                    FROM information_schema.REFERENTIAL_CONSTRAINTS
                    WHERE CONSTRAINT_SCHEMA = DATABASE()
                      AND TABLE_NAME = 'crescimento_bacteriano'
                      AND CONSTRAINT_NAME = 'fk_crescimento_simulacao'
                    """
                )
                assert cursor.fetchone() == ("CASCADE",)

                # As duas simulações devem coexistir: o histórico foi preservado
                cursor.execute(
                    """
                    SELECT id, populacao_inicial, quantidade_periodos
                    FROM simulacoes_bacterianas
                    WHERE id IN (%s, %s)
                    ORDER BY id
                    """,
                    (primeira_id, segunda_id),
                )
                assert cursor.fetchall() == (
                    (primeira_id, primeira_populacao, 3),
                    (segunda_id, segunda_populacao, 2),
                )

                # Confirma que a coluna nova existe e a antiga foi removida
                cursor.execute(
                    """
                    SELECT COLUMN_NAME
                    FROM information_schema.COLUMNS
                    WHERE TABLE_SCHEMA = DATABASE()
                      AND TABLE_NAME = 'crescimento_bacteriano'
                      AND COLUMN_NAME IN (
                          'populacaoperiodo',
                          'populacao_periodo'
                      )
                    """
                )
                assert {linha[0] for linha in cursor.fetchall()} == {
                    "populacao_periodo"
                }

                # Confirma os períodos registrados em cada simulação
                cursor.execute(
                    """
                    SELECT periodo, populacao_periodo
                    FROM crescimento_bacteriano
                    WHERE simulacao_id = %s
                    ORDER BY periodo
                    """,
                    (primeira_id,),
                )
                assert cursor.fetchall() == ((1, 3), (2, 6), (3, 12))

                cursor.execute(
                    """
                    SELECT periodo, populacao_periodo
                    FROM crescimento_bacteriano
                    WHERE simulacao_id = %s
                    ORDER BY periodo
                    """,
                    (segunda_id,),
                )
                assert cursor.fetchall() == ((1, 11), (2, 22))

                # A chave estrangeira deve rejeitar uma simulação inexistente
                cursor.execute(
                    """
                    SELECT COALESCE(MAX(id), 0) + 1000000
                    FROM simulacoes_bacterianas
                    """
                )
                id_inexistente = cursor.fetchone()[0]

                with pytest.raises(pymysql.err.IntegrityError):
                    cursor.execute(
                        """
                        INSERT INTO crescimento_bacteriano (
                            simulacao_id,
                            periodo,
                            populacao_periodo
                        )
                        VALUES (%s, %s, %s)
                        """,
                        (id_inexistente, 1, 1),
                    )

                conexao.rollback()

                # Excluir uma simulação deve excluir seus períodos em cascata
                cursor.execute(
                    "DELETE FROM simulacoes_bacterianas WHERE id = %s",
                    (primeira_id,),
                )
                conexao.commit()

                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM crescimento_bacteriano
                    WHERE simulacao_id = %s
                    """,
                    (primeira_id,),
                )
                assert cursor.fetchone() == (0,)

                # A segunda simulação e seus resultados devem continuar intactos
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM simulacoes_bacterianas
                    WHERE id = %s
                    """,
                    (segunda_id,),
                )
                assert cursor.fetchone() == (1,)

                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM crescimento_bacteriano
                    WHERE simulacao_id = %s
                    """,
                    (segunda_id,),
                )
                assert cursor.fetchone() == (2,)

        finally:
            conexao.close()

    finally:
        # Remove somente as simulações criadas por esta execução do teste
        if simulacao_ids:
            conexao_limpeza = conectar()

            try:
                with conexao_limpeza.cursor() as cursor:
                    cursor.executemany(
                        "DELETE FROM simulacoes_bacterianas WHERE id = %s",
                        [(simulacao_id,) for simulacao_id in simulacao_ids],
                    )

                conexao_limpeza.commit()

            finally:
                conexao_limpeza.close()
