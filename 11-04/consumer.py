import pika

username = 'test'
password = 'test'

credentials = pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
channel = connection.channel()


try:
    queue_declare_ok = channel.queue_declare(queue='hello', passive=True)
except pika.exceptions.ChannelClosedByBroker as e:
    error_code, error_text = e.args
    if error_code == 406:
        print(f"Очередь 'hello' уже существует с другими параметрами: {error_text}")
        
        queue_declare_ok = channel.queue_declare(queue='hello', durable=True)
    else:
        print(f"Ошибка при объявлении очереди: {error_code} - {error_text}")
        raise e
else:
    queue_name = queue_declare_ok.method.queue

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()
