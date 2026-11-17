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
