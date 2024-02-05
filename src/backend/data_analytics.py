import pika
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import ast

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE = 'bitcoin_volume_queue'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BTC.sqlite3'
app.app_context().push()
db = SQLAlchemy(app)

class BTC(db.Model):
    time = db.Column(db.Integer, primary_key=True)
    volume = db.Column(db.Integer,  default=0)

def store_volume_data(json_data):
    json_data = ast.literal_eval(json_data.decode('utf-8'))
    if 'live-2h-chart' in json_data:
        db.create_all()
        data = sum(json_data['live-2h-chart']['vsizes'])
        row_entry = BTC(time=json_data['live-2h-chart']['added'], volume=data)
        db.session.add(row_entry)
        db.session.commit()
        print(f"Data inserted {row_entry}")

def callback(ch, method, properties, body):
    store_volume_data(body)

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