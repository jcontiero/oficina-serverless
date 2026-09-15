from unittest.mock import patch, MagicMock
from auth.repository import buscar_cliente_por_cpf, ClienteDB

def test_buscar_cliente_sem_database_url():
    with patch.dict("os.environ", {}, clear=True):
        res = buscar_cliente_por_cpf("12345678901", db_url=None)
        assert res is None

def test_buscar_cliente_com_sucesso():
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ("id-123", "Cliente Teste", "12345678901", "teste@email.com", "ATIVO")

    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    with patch("psycopg.connect", return_value=mock_conn) as mock_connect:
        res = buscar_cliente_por_cpf("12345678901", db_url="postgresql+psycopg://user:pass@host:5432/db")
        assert res is not None
        assert res.id == "id-123"
        assert res.nome == "Cliente Teste"
        assert res.cpf == "12345678901"
        assert res.email == "teste@email.com"
        assert res.status == "ATIVO"
        # Verifica normalização de url
        mock_connect.assert_called_once_with("postgresql://user:pass@host:5432/db")

def test_buscar_cliente_normalizacao_pg8000():
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None

    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    mock_conn.__enter__.return_value = mock_conn

    with patch("psycopg.connect", return_value=mock_conn) as mock_connect:
        res = buscar_cliente_por_cpf("12345678901", db_url="postgresql+pg8000://user:pass@host:5432/db")
        assert res is None
        mock_connect.assert_called_once_with("postgresql://user:pass@host:5432/db")
