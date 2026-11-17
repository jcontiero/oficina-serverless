import os
from dataclasses import dataclass
from typing import Callable

import httpx


@dataclass
class ClienteDB:
    id: str
    nome: str
    cpf: str
    email: str
    status: str


class ErroComunicacaoOsServiceError(Exception):
    """Falha transitória ou indisponibilidade ao consultar o endpoint interno do OS Service."""


def obter_google_oidc_token(
    audience: str,
    fetcher: Callable[[str], str] | None = None,
) -> str:
    """
    Obtém um Google OIDC ID Token para autenticar a chamada da Cloud Function ao
    endpoint interno POST /internal/clientes/autenticacao do OS Service.
    Em ambiente local de teste, aceita token injetado via OS_INTERNAL_OIDC_TOKEN
    ou fetcher customizado.
    """
    if fetcher is not None:
        return fetcher(audience)

    token_estatico = os.getenv("OS_INTERNAL_OIDC_TOKEN")
    if token_estatico:
        return token_estatico

    from google.auth.transport.requests import Request
    from google.oauth2 import id_token

    return id_token.fetch_id_token(Request(), audience)


def buscar_cliente_por_cpf(
    cpf: str,
    *,
    lookup_url: str | None = None,
    lookup_audience: str | None = None,
    http_client: httpx.Client | None = None,
    token_fetcher: Callable[[str], str] | None = None,
    timeout_seconds: float = 5.0,
) -> ClienteDB | None:
    """
    Consulta o cliente pelo CPF via HTTP interno autenticado no OS Service
    (POST /internal/clientes/autenticacao), sem qualquer acesso direto ao banco SQL.
    """
    url = lookup_url or os.getenv("OS_AUTH_LOOKUP_URL")
    if not url:
        return None

    audience = lookup_audience or os.getenv("OS_AUTH_LOOKUP_AUDIENCE") or url
    try:
        oidc_token = obter_google_oidc_token(audience, fetcher=token_fetcher)
    except Exception as exc:
        raise ErroComunicacaoOsServiceError(
            f"Falha ao obter ID token OIDC para {audience}: {exc}"
        ) from exc

    headers = {
        "Authorization": f"Bearer {oidc_token}",
        "Content-Type": "application/json",
    }
    payload = {"cpf": cpf}

    try:
        if http_client is not None:
            resp = http_client.post(
                url, json=payload, headers=headers, timeout=timeout_seconds
            )
        else:
            with httpx.Client(timeout=timeout_seconds) as client:
                resp = client.post(url, json=payload, headers=headers)
    except httpx.HTTPError as exc:
        raise ErroComunicacaoOsServiceError(
            f"Erro de rede ao consultar OS Service em {url}: {exc}"
        ) from exc

    if resp.status_code == 404:
        return None

    if resp.status_code >= 400:
        raise ErroComunicacaoOsServiceError(
            f"Resposta inesperada do OS Service ({resp.status_code}): {resp.text}"
        )

    dados = resp.json()
    return ClienteDB(
        id=str(dados["id"]),
        nome=str(dados.get("nome", "")),
        cpf=str(dados.get("cpf", cpf)),
        email=str(dados.get("email", "")),
        status=str(dados["status"]),
    )
