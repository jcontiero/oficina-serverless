import json
from unittest.mock import MagicMock, patch
from flask import Request
from auth.handler import auth_handler
from auth.repository import ClienteDB

def criar_mock_request(path="/", method="GET", body=None):
    req = MagicMock(spec=Request)
    req.path = path
    req.method = method
    req.get_json.return_value = body or {}
    return req

def test_handler_jwks():
    req = criar_mock_request(path="/.well-known/jwks.json", method="GET")
    resp = auth_handler(req)
    assert resp.status_code == 200
    data = json.loads(resp.get_data())
    assert "keys" in data

def test_handler_health():
    req = criar_mock_request(path="/health", method="GET")
    resp = auth_handler(req)
    assert resp.status_code == 200
    data = json.loads(resp.get_data())
    assert data["status"] == "healthy"

def test_handler_cpf_invalido():
    req = criar_mock_request(path="/auth/cpf", method="POST", body={"cpf": "11111111111"})
    resp = auth_handler(req)
    assert resp.status_code == 400

@patch("auth.handler.buscar_cliente_por_cpf")
def test_handler_cliente_nao_encontrado(mock_buscar):
    mock_buscar.return_value = None
    req = criar_mock_request(path="/auth/cpf", method="POST", body={"cpf": "52998224725"})
    resp = auth_handler(req)
    assert resp.status_code == 404

@patch("auth.handler.buscar_cliente_por_cpf")
def test_handler_cliente_inativo(mock_buscar):
    mock_buscar.return_value = ClienteDB(
        id="123", nome="Inativo", cpf="52998224725", email="inativo@teste.com", status="INATIVO"
    )
    req = criar_mock_request(path="/auth/cpf", method="POST", body={"cpf": "52998224725"})
    resp = auth_handler(req)
    assert resp.status_code == 403

@patch("auth.handler.buscar_cliente_por_cpf")
def test_handler_autenticacao_sucesso(mock_buscar):
    mock_buscar.return_value = ClienteDB(
        id="12345", nome="Ativo", cpf="52998224725", email="ativo@teste.com", status="ATIVO"
    )
    req = criar_mock_request(path="/auth/cpf", method="POST", body={"cpf": "52998224725"})
    resp = auth_handler(req)
    assert resp.status_code == 200
    data = json.loads(resp.get_data())
    assert "access_token" in data
    assert data["actor_type"] == "CLIENTE"

def test_handler_options_cors():
    req = criar_mock_request(path="/auth/cpf", method="OPTIONS")
    resp = auth_handler(req)
    assert resp.status_code == 204
    assert resp.headers.get("Access-Control-Allow-Origin") == "*"

def test_handler_metodo_nao_permitido():
    req = criar_mock_request(path="/auth/cpf", method="GET")
    resp = auth_handler(req)
    assert resp.status_code == 405
