import pytest

from main import conectar, obter_certificado_ssl


def test_db_ssl_ca_obrigatorio(monkeypatch):
    """A conexão segura não pode funcionar sem DB_SSL_CA."""
    monkeypatch.delenv("DB_SSL_CA", raising=False)

    with pytest.raises(ValueError, match="DB_SSL_CA"):
        obter_certificado_ssl()


def test_certificado_ssl_deve_existir(monkeypatch, tmp_path):
    """DB_SSL_CA deve apontar para um arquivo existente."""
    certificado_inexistente = tmp_path / "certificado-inexistente.pem"
    monkeypatch.setenv("DB_SSL_CA", str(certificado_inexistente))

    with pytest.raises(FileNotFoundError, match="Certificado SSL não encontrado"):
        obter_certificado_ssl()


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
