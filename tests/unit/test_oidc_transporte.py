from unittest.mock import patch

from auth.repository import obter_google_oidc_token


def test_obter_token_utiliza_transporte_requests_instalado(monkeypatch):
    monkeypatch.delenv("OS_INTERNAL_OIDC_TOKEN", raising=False)
    with patch("google.oauth2.id_token.fetch_id_token", return_value="token-de-teste") as fetch:
        token = obter_google_oidc_token("https://api.oficina.internal/internal/clientes/autenticacao")
    assert token == "token-de-teste"
    assert fetch.call_args.args[1] == "https://api.oficina.internal/internal/clientes/autenticacao"
    assert callable(fetch.call_args.args[0])
