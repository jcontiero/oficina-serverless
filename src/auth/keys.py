import os
import base64
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

KEY_ID = os.getenv("JWT_KEY_ID", "oficina-rsa-key-2026")

# Chave privada gerada em runtime ou carregada via ambiente
_PRIVATE_KEY_PEM = os.getenv("JWT_PRIVATE_KEY_PEM")
if _PRIVATE_KEY_PEM:
    private_key = serialization.load_pem_private_key(
        _PRIVATE_KEY_PEM.encode(),
        password=None
    )
else:
    # Gerar par de chaves RSA de 2048 bits para a sessao/runtime
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

public_key = private_key.public_key()

def get_private_key():
    return private_key

def get_public_key():
    return public_key

def get_jwk() -> dict:
    public_numbers = public_key.public_numbers()
    def _int_to_base64(n: int) -> str:
        b = n.to_bytes((n.bit_length() + 7) // 8, byteorder="big")
        return base64.urlsafe_b64encode(b).decode("utf-8").rstrip("=")

    return {
        "kty": "RSA",
        "use": "sig",
        "alg": "RS256",
        "kid": KEY_ID,
        "n": _int_to_base64(public_numbers.n),
        "e": _int_to_base64(public_numbers.e),
    }
