import re
from pathlib import Path

GATEWAY_SPEC = (
    Path(__file__).resolve().parents[2] / "openapi" / "gateway.yaml"
).read_text(encoding="utf-8")


ROTAS_PARAMETRIZADAS = (
    "/ordens-de-servico/{id}",
    "/v1/ordens-servico/{id}",
    "/v1/ordens-servico/{id}/saga",
    "/v1/ordens-servico/{id}/cancelar",
    "/v1/ordens-servico/{id}/saga/reprocessar-estorno",
    "/v1/ordens-servico/{id}/nova-rodada",
    "/v1/orcamentos/{id}/decisao",
    "/v1/orcamentos/por-os/{os_id}",
    "/v1/pagamentos/por-os/{os_id}",
    "/v1/execucoes/{id}/diagnostico",
    "/v1/execucoes/{id}/iniciar",
    "/v1/execucoes/{id}/concluir",
    "/v1/pecas/{id}",
    "/v1/ordens-servico/{id}/entrega",
    "/v1/execucoes/{id}",
)


def test_rotas_parametrizadas_delegam_traducao_do_caminho_ao_gateway():
    assert not re.search(r'address: "https://\$\{[^}]+\}/[^"\n]*/\{', GATEWAY_SPEC)

    for rota in ROTAS_PARAMETRIZADAS:
        inicio = GATEWAY_SPEC.index(f"  {rota}:")
        proxima_rota = GATEWAY_SPEC.find("\n  /", inicio + 1)
        bloco = GATEWAY_SPEC[inicio : proxima_rota if proxima_rota > 0 else None]
        assert 'path_translation: "APPEND_PATH_TO_ADDRESS"' in bloco, rota

