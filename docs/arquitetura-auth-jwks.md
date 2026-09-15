# Arquitetura: Autenticação por CPF e JWKS (Serverless)

## 1. Visão Geral
A autenticação do ator **CLIENTE** foi desacoplada do monolito e implementada como uma **Cloud Function serverless**, garantindo escalabilidade, segurança e isolamento de responsabilidades.

```mermaid
sequenceDiagram
    autonumber
    actor Cliente
    participant Gateway as API Gateway / Cloud Function
    participant DB as Cloud SQL (PostgreSQL)
    participant API as Oficina API (GKE)

    Cliente->>Gateway: POST /auth/cpf {"cpf": "529.982.247-25"}
    Note over Gateway: 1. Valida digitos verificadores do CPF
    Gateway->>DB: 2. SELECT cliente WHERE cpf = :cpf (via VPC Connector)
    alt Cliente Inexistente
        DB-->>Gateway: Not Found
        Gateway-->>Cliente: 404 Not Found
    else Cliente Inativo
        DB-->>Gateway: status = INATIVO
        Gateway-->>Cliente: 403 Forbidden
    else Cliente Ativo
        DB-->>Gateway: status = ATIVO, id = UUID
        Note over Gateway: 3. Assina JWT com Chave Privada RSA (RS256)
        Gateway-->>Cliente: 200 OK {"access_token": "ey...", "token_type": "bearer"}
    end

    Note over Cliente,API: Uso do Token nas rotas de cliente (ex: /ordens-de-servico)
    Cliente->>API: GET /ordens-de-servico (Authorization: Bearer <token>)
    API->>Gateway: GET /.well-known/jwks.json (Chave Publica)
    Note over API: Valida assinatura assimetrica, aud, iss e ownership
    API-->>Cliente: 200 OK (Dados da OS)
```

## 2. Padrões de Segurança
- **Assinatura Assimétrica (RS256)**: Apenas a Cloud Function possui a chave privada RSA. Qualquer serviço (como a API ou o API Gateway) valida os tokens usando exclusivamente a chave pública distribuída via JWKS.
- **Formato JWKS (RFC 7517)**: Exposto em `/.well-known/jwks.json` com `kty: RSA`, `use: sig`, `alg: RS256` e identificador de chave (`kid`).
- **Comunicação Privada com o Banco**: A Cloud Function utiliza o **Serverless VPC Access connector** para alcançar o Cloud SQL exclusivamente através da rede VPC por IP privado (`10.0.0.0/20`), sem expor o banco à internet pública.
