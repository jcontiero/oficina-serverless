from src.auth.keys import get_jwk

def obter_jwks() -> dict:
    return {
        "keys": [get_jwk()]
    }
