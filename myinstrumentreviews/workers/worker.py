# Background Worker (Consumer)
#TO BE IMPLEMENTED SOON WITH RABBITMQ


import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the exchange
channel.exchange_declare(exchange='reviews', exchange_type='direct')

# Declare a queue
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Bind the queue to the exchange with the routing key
channel.queue_bind(exchange='reviews', queue=queue_name, routing_key='new_review')

def callback(ch, method, properties, body):
    # Handle the message (e.g., update sentiment analysis score, update the database)
    print(f"Received message: {body}")

# Set up the callback function
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
