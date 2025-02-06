CREATE DATABASE IF NOT EXISTS url_shortener;

CREATE TABLE IF NOT EXISTS url_shortener.clicks_queue (
    short_code String,
    ip_address String,
    user_agent String,
    referrer String,
    timestamp DateTime DEFAULT now()
) ENGINE = RabbitMQ 
SETTINGS rabbitmq_host_port = 'rabbitmq:5672',
         rabbitmq_exchange_name = 'clicks',
         rabbitmq_format = 'JSONEachRow';
