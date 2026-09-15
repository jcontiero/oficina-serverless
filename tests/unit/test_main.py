from unittest.mock import patch, MagicMock
import src.main as main_mod

def test_main_auth_handler():
    mock_req = MagicMock()
    with patch("src.main.auth_handler_impl") as mock_impl:
        mock_impl.return_value = "ok"
        res = main_mod.auth_handler(mock_req)
        mock_impl.assert_called_once_with(mock_req)
        assert res == "ok"

def test_main_notificacoes_handler():
    mock_event = MagicMock()
    mock_event.data = {"test": "data"}
    with patch("src.main.notificacoes_handler_impl") as mock_impl:
        mock_impl.return_value = "handled"
        res = main_mod.notificacoes_handler(mock_event)
        mock_impl.assert_called_once_with({"test": "data"}, None)
        assert res == "handled"
