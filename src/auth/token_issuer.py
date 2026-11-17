import datetime
import os

import jwt

from auth.keys import KEY_ID, get_private_key

ENV = os.getenv("ENVIRONMENT", "homolog")
ISSUER = os.getenv("JWT_ISSUER", f"oficina-auth-{ENV}")
AUDIENCE = os.getenv("JWT_AUDIENCE", f"oficina-backend-{ENV}")
EXPIRES_IN_MINUTES = 60


def emitir_token_cliente(
    cliente_id: str,
    cpf: str,
    *,
    issuer: str | None = None,
    audience: str | None = None,
) -> dict:
    agora = datetime.datetime.now(datetime.UTC)
    expiracao = agora + datetime.timedelta(minutes=EXPIRES_IN_MINUTES)

    iss_efetivo = issuer or ISSUER
    aud_efetivo = audience or AUDIENCE

    payload = {
        "sub": str(cliente_id),
        "cpf": str(cpf),
        "actor_type": "CLIENTE",
        "roles": ["CLIENTE"],
        "iss": iss_efetivo,
        "aud": aud_efetivo,
        "iat": int(agora.timestamp()),
        "exp": int(expiracao.timestamp()),
    }

    headers = {
        "kid": KEY_ID,
        "alg": "RS256",
        "typ": "JWT",
    }

    token = jwt.encode(
        payload,
        get_private_key(),
        algorithm="RS256",
        headers=headers,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": EXPIRES_IN_MINUTES * 60,
        "cliente_id": str(cliente_id),
        "actor_type": "CLIENTE",
    }
