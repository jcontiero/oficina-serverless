from auth.keys import get_private_key, get_public_key, get_jwk
from auth.jwks import obter_jwks

def test_chaves_rsa():
    assert get_private_key() is not None
    assert get_public_key() is not None

def test_jwk_format():
    jwk = get_jwk()
    assert jwk["kty"] == "RSA"
    assert jwk["use"] == "sig"
    assert jwk["alg"] == "RS256"
    assert "kid" in jwk
    assert "n" in jwk
    assert "e" in jwk

def test_obter_jwks():
    jwks = obter_jwks()
    assert "keys" in jwks
    assert len(jwks["keys"]) == 1
    assert jwks["keys"][0]["alg"] == "RS256"
