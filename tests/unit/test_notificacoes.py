import base64
import json
import pytest
from notificacoes.main import notificacoes_handler

def test_notificacoes_handler_sem_data():
    event = {}
    # Não deve levantar exceção
    notificacoes_handler(event, None)

def test_notificacoes_handler_sucesso():
    payload = {
        "status_novo": "Aguardando Aprovação",
        "os_id": "os-123"
    }
    encoded = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
    event = {
        "data": encoded,
        "attributes": {"tipo_evento": "STATUS_ALTERADO"}
    }
    notificacoes_handler(event, None)

def test_notificacoes_handler_erro_json():
    event = {
        "data": base64.b64encode(b"invalid-json").decode("utf-8")
    }
    with pytest.raises(Exception):
        notificacoes_handler(event, None)
