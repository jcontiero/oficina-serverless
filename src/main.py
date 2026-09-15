import functions_framework
from auth.handler import auth_handler as auth_handler_impl
from notificacoes.main import notificacoes_handler as notificacoes_handler_impl

@functions_framework.http
def auth_handler(request):
    return auth_handler_impl(request)

@functions_framework.cloud_event
def notificacoes_handler(cloud_event):
    # O handler de notificacoes espera cloud_event (Pub/Sub Eventarc)
    return notificacoes_handler_impl(cloud_event.data, None)
