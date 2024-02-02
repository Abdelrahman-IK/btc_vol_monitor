import pika


RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE = 'bitcoin_volume_queue'

def callback(ch, method, properties, body):
    print(f"Received message from RabbitMQ: {body}")

def consume_from_rabbitmq():
    connection_params = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
    )

    with pika.BlockingConnection(connection_params) as connection:
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE)
        channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
        print("Waiting for messages. To exit, press Ctrl+C")
        channel.start_consuming()

if __name__ == "__main__":
    consume_from_rabbitmq()