import jwt
from auth.token_issuer import emitir_token_cliente, ISSUER, AUDIENCE
from auth.keys import get_public_key

def test_emitir_token_cliente():
    cliente_id = "550e8400-e29b-41d4-a716-446655440000"
    cpf = "52998224725"

    resultado = emitir_token_cliente(cliente_id, cpf)
    assert "access_token" in resultado
    assert resultado["token_type"] == "bearer"
    assert resultado["cliente_id"] == cliente_id
    assert resultado["actor_type"] == "CLIENTE"

    # Validar e decodificar token com a chave publica
    token = resultado["access_token"]
    payload = jwt.decode(
        token,
        get_public_key(),
        algorithms=["RS256"],
        audience=AUDIENCE,
        issuer=ISSUER
    )

    assert payload["sub"] == cliente_id
    assert payload["cpf"] == cpf
    assert payload["actor_type"] == "CLIENTE"
    assert "CLIENTE" in payload["roles"]
