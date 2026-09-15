# ADR-001: Ponto de Entrada Único — Google API Gateway vs Cloud Load Balancer (GKE Ingress)

## Status
**Aprovado**

## Contexto
O Tech Challenge exige a definição de um ponto de entrada público e único para o sistema da oficina mecânica, integrando:
1. **Componentes Serverless**: Cloud Function de autenticação por CPF e endpoint JWKS.
2. **Componentes GKE**: APIs principais de atendimento, catálogo, estoque, identidade de funcionários e relatórios.

## Alternativas Avaliadas

### Alternativa 1: Google Cloud API Gateway (Baseado em OpenAPI / Envoy)
- **Prós**:
  - Totalmente gerenciado e serverless (escala a zero).
  - Roteamento nativo baseado em especificação OpenAPI (`x-google-backend`).
  - Suporte nativo à validação de chaves de API e integração com Cloud Functions e Cloud Run.
  - Custo baixo para ambientes com tráfego sob demanda (Tech Challenge).
- **Contras**:
  - Exige que o backend GKE seja exposto através de IP público, Cloud Armor ou Load Balancer com DNS público interno.

### Alternativa 2: Cloud Application Load Balancer Externo (GKE Ingress + Serverless NEGs)
- **Prós**:
  - Suporta roteamento de caminhos (URL Maps) direto para Pods via Network Endpoint Groups (NEGs) e Serverless NEGs.
  - Integração profunda com Cloud Armor e certificados SSL gerenciados pelo Google.
- **Contras**:
  - Custo fixo mensal por regras de encaminhamento do Load Balancer (Forwarding Rules).

## Decisão
Adotamos a **especificação OpenAPI com Google API Gateway** como a interface pública padrão documentada e declarativa, com suporte complementar a **GKE Ingress / Cloud Load Balancer** para ambientes de alta volumetria.
