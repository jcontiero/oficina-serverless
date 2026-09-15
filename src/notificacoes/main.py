import base64
import json
import logging
import smtplib
import os
from email.message import EmailMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("notificacoes")

def notificacoes_handler(event, context):
    """
    Background Cloud Function triggered by Pub/Sub.
    Eventarc sends the Pub/Sub message in the event data.
    """
    logger.info(f"Recebido evento: {event}")
    
    if 'data' in event:
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        try:
            payload = json.loads(pubsub_message)
            logger.info(f"Payload parseado: {payload}")
            
            tipo_evento = event.get('attributes', {}).get('tipo_evento', '')
            status_novo = payload.get('status_novo')
            os_id = payload.get('os_id')
            
            # Aqui deveriamos buscar o e-mail do cliente no banco.
            # Como a função tem acesso ao BD (via VPC), podemos usar psycopg2 ou simular.
            # Para o Tech Challenge, vamos mockar o envio de e-mail ou usar log.
            
            if status_novo == "Aguardando Aprovação":
                link_aprovacao = f"https://api.oficina.com/os/{os_id}/aprovar"
                logger.info(f"ENVIANDO EMAIL PARA CLIENTE. OS {os_id} aguardando aprovação: {link_aprovacao}")
                # Mock envio real SMTP (na pratica usariamos um serviço como SendGrid ou SMTP lib)
                
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            raise e
    else:
        logger.warning("Evento sem data")
