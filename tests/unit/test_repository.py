from unittest.mock import patch

import httpx
import pytest

from auth.repository import (
    ErroComunicacaoOsServiceError,
    buscar_cliente_por_cpf,
    obter_google_oidc_token,
)


def test_buscar_cliente_sem_lookup_url():
    with patch.dict("os.environ", {}, clear=True):
        res = buscar_cliente_por_cpf("12345678901", lookup_url=None)
        assert res is None


def test_buscar_cliente_via_http_interno_com_sucesso():
    chamadas: list[tuple[str, dict[str, str]]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        chamadas.append((str(request.url), dict(request.headers)))
        return httpx.Response(
            200,
            json={
                "id": "id-123",
                "nome": "Cliente Teste",
                "cpf": "12345678901",
                "email": "teste@email.com",
                "status": "ATIVO",
            },
        )

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        res = buscar_cliente_por_cpf(
            "12345678901",
            lookup_url="https://api.oficina.internal/internal/clientes/autenticacao",
            lookup_audience="https://api.oficina.internal/internal/clientes/autenticacao",
            http_client=client,
            token_fetcher=lambda aud: f"oidc-token-for-{aud}",
        )
        assert res is not None
        assert res.id == "id-123"
        assert res.nome == "Cliente Teste"
        assert res.cpf == "12345678901"
        assert res.email == "teste@email.com"
        assert res.status == "ATIVO"
        assert chamadas[0][1]["authorization"].startswith("Bearer oidc-token-for-")


def test_buscar_cliente_404_retorna_none():
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, json={"detail": "Not found"})

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        res = buscar_cliente_por_cpf(
            "12345678901",
            lookup_url="https://api.oficina.internal/internal/clientes/autenticacao",
            http_client=client,
            token_fetcher=lambda _aud: "oidc-tok",
        )
        assert res is None


def test_buscar_cliente_erro_500_ou_rede_levanta_excecao():
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, text="Unavailable")

    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(ErroComunicacaoOsServiceError, match="503"):
            buscar_cliente_por_cpf(
                "12345678901",
                lookup_url="https://api.oficina.internal/internal/clientes/autenticacao",
                http_client=client,
                token_fetcher=lambda _aud: "oidc-tok",
            )


def test_obter_google_oidc_token_via_env():
    with patch.dict("os.environ", {"OS_INTERNAL_OIDC_TOKEN": "tok-env-123"}):
        assert obter_google_oidc_token("aud-1") == "tok-env-123"


def test_obter_google_oidc_token_via_google_auth():
    import sys
    from types import SimpleNamespace

    fake_requests = SimpleNamespace(Request=lambda: object())
    fake_id_token = SimpleNamespace(fetch_id_token=lambda _req, _aud: "tok-gcp")
    fake_oauth2 = SimpleNamespace(id_token=fake_id_token)
    fake_transport = SimpleNamespace(requests=fake_requests)
    with patch.dict("os.environ", {}, clear=True):
        with patch.dict(
            sys.modules,
            {
                "google.auth.transport": fake_transport,
                "google.auth.transport.requests": fake_requests,
                "google.oauth2": fake_oauth2,
                "google.oauth2.id_token": fake_id_token,
            },
        ):
            assert obter_google_oidc_token("https://os.internal") == "tok-gcp"


def test_buscar_cliente_falha_oidc_e_erro_rede_sem_client_injetado():
    with pytest.raises(ErroComunicacaoOsServiceError):
        buscar_cliente_por_cpf(
            "52998224725",
            lookup_url="https://os.internal/internal/clientes/autenticacao",
            token_fetcher=lambda _aud: (_ for _ in ()).throw(RuntimeError("sem oidc")),
        )

    class _FakeClient:
        def __init__(self, timeout: float = 5.0) -> None:
            self.timeout = timeout

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def post(self, *_args, **_kwargs):
            raise httpx.ConnectError("rede indisponivel")

    with patch("auth.repository.httpx.Client", _FakeClient):
        with pytest.raises(ErroComunicacaoOsServiceError):
            buscar_cliente_por_cpf(
                "52998224725",
                lookup_url="https://os.internal/internal/clientes/autenticacao",
                token_fetcher=lambda _aud: "oidc-ok",
            )
