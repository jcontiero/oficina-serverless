import datetime
import jwt
from src.auth.keys import get_private_key, KEY_ID

ISSUER = "oficina-auth-serverless"
AUDIENCE = "oficina-api"
EXPIRES_IN_MINUTES = 60

def emitir_token_cliente(cliente_id: str, cpf: str) -> dict:
    agora = datetime.datetime.now(datetime.timezone.utc)
    expiracao = agora + datetime.timedelta(minutes=EXPIRES_IN_MINUTES)

    payload = {
        "sub": str(cliente_id),
        "cpf": str(cpf),
        "actor_type": "CLIENTE",
        "roles": ["CLIENTE"],
        "iss": ISSUER,
        "aud": AUDIENCE,
        "iat": int(agora.timestamp()),
        "exp": int(expiracao.timestamp()),
    }

    headers = {
        "kid": KEY_ID,
        "alg": "RS256",
        "typ": "JWT"
    }

    token = jwt.encode(
        payload,
        get_private_key(),
        algorithm="RS256",
        headers=headers
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": EXPIRES_IN_MINUTES * 60,
        "cliente_id": str(cliente_id),
        "actor_type": "CLIENTE"
    }
