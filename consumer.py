import json

import pika

params = pika.ConnectionParameters(host='localhost')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='order')


def callback(ch, method, properties, body):
    print('Received')
    order = json.loads(body)
    print(order)
    print('Order was created')


channel.basic_consume(queue='order', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()