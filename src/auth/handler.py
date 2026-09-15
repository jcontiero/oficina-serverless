import json
import functions_framework
from flask import Request, Response
from auth.cpf import limpar_cpf, validar_cpf
from auth.jwks import obter_jwks
from auth.token_issuer import emitir_token_cliente
from auth.repository import buscar_cliente_por_cpf

@functions_framework.http
def auth_handler(request: Request) -> Response:
    # CORS Preflight
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Max-Age': '3600'
        }
        return Response('', status=204, headers=headers)
        
    cors_headers = {'Access-Control-Allow-Origin': '*'}

    # 1. Endpoint JWKS
    if request.path.endswith("/.well-known/jwks.json") or request.path == "/jwks":
        return Response(
            json.dumps(obter_jwks()),
            status=200,
            mimetype="application/json",
            headers=cors_headers
        )

    # 2. Health check
    if request.path == "/health":
        return Response(
            json.dumps({"status": "healthy", "service": "oficina-auth-serverless"}),
            status=200,
            mimetype="application/json",
            headers=cors_headers
        )

    # 3. Autenticacao por CPF (POST)
    if request.method == "POST":
        try:
            data = request.get_json(silent=True) or {}
            cpf_bruto = data.get("cpf", "")
            cpf_limpo = limpar_cpf(cpf_bruto)

            if not validar_cpf(cpf_limpo):
                return Response(
                    json.dumps({"detail": "CPF informado é inválido."}),
                    status=400,
                    mimetype="application/json",
                    headers=cors_headers
                )

            cliente = buscar_cliente_por_cpf(cpf_limpo)
            if not cliente:
                return Response(
                    json.dumps({"detail": "Cliente não cadastrado na base de dados."}),
                    status=404,
                    mimetype="application/json",
                    headers=cors_headers
                )

            if cliente.status.upper() != "ATIVO":
                return Response(
                    json.dumps({"detail": "Cadastro do cliente inativo ou suspenso."}),
                    status=403,
                    mimetype="application/json",
                    headers=cors_headers
                )

            token_response = emitir_token_cliente(cliente.id, cliente.cpf)
            return Response(
                json.dumps(token_response),
                status=200,
                mimetype="application/json",
                headers=cors_headers
            )

        except Exception as e:
            return Response(
                json.dumps({"detail": f"Erro interno ao processar autenticação: {str(e)}"}),
                status=500,
                mimetype="application/json",
                headers=cors_headers
            )

    return Response(
        json.dumps({"detail": "Método não permitido ou rota inexistente."}),
        status=405,
        mimetype="application/json",
        headers=cors_headers
    )
