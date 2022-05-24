import pika,json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE","admin.settings")
django.setup()

from products.models import Product



params=pika.URLParameters("amqps://udrtfoht:eUowJnkHLUKeQC2VG-w25KD3T3xWOF8r@beaver.rmq.cloudamqp.com/udrtfoht")

connection = pika.BlockingConnection(params)

channel= connection.channel()

channel.queue_declare(queue="admin")

def callback(ch, method, properties, body):
    print("Received in admin")
    data=json.loads(body)
    print(data)
    product = Product.objects.get(id=id)
    product.likes+=1
    product.save()
    print("Product likes increased")
    

channel.basic_consume(queue="admin",on_message_callback=callback, auto_ack=True)

print("\nStarted consuming\n")

channel.start_consuming()

channel.close()
