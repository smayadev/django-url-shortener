CREATE DATABASE IF NOT EXISTS url_shortener;

CREATE TABLE IF NOT EXISTS url_shortener.clicks_persistent (
    short_code String,
    ip_address String,
    user_agent String,
    referrer String,
    timestamp DateTime
) ENGINE = MergeTree()
ORDER BY (short_code, timestamp);

CREATE TABLE IF NOT EXISTS url_shortener.clicks_queue (
    short_code String,
    ip_address String,
    user_agent String,
    referrer String,
    timestamp DateTime DEFAULT now()
) ENGINE = RabbitMQ
SETTINGS 
    rabbitmq_host_port = 'rabbitmq:5672',
    rabbitmq_exchange_name = 'clicks',
    rabbitmq_format = 'JSONEachRow',
    rabbitmq_queue_base = 'clicks_queue',
    rabbitmq_num_consumers = 1,
    rabbitmq_username = 'guest',
    rabbitmq_password = 'guest';

CREATE MATERIALIZED VIEW IF NOT EXISTS url_shortener.clicks_mv TO url_shortener.clicks_persistent AS
SELECT *
FROM url_shortener.clicks_queue;
