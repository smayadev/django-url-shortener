import pika
import json
from celery import shared_task
from django.utils.timezone import now
from django.conf import settings

@shared_task
def send_click_to_rabbitmq(short_code, ip_address, user_agent, referrer):
    """
    Sends click data to RabbitMQ asynchronously
    """
    click_data = {
        "short_code": short_code,
        "ip_address": ip_address,
        "user_agent": user_agent,
        "referrer": referrer,
        "timestamp": now().isoformat()
    }

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
        channel = connection.channel()
        channel.exchange_declare(exchange="clicks", exchange_type="fanout")
        channel.basic_publish(exchange="clicks", routing_key="", body=json.dumps(click_data))
        connection.close()
    except Exception as e:
        print(f"Failed to send click data to RabbitMQ: {e}")
