import pika,json
from main import Product,db


params=pika.URLParameters("amqps://udrtfoht:eUowJnkHLUKeQC2VG-w25KD3T3xWOF8r@beaver.rmq.cloudamqp.com/udrtfoht")

connection = pika.BlockingConnection(params)

channel= connection.channel()

channel.queue_declare(queue="main")

def callback(ch, method, properties, body):
    print("Received in main")
    data = json.loads(body)
    print(data)
    if properties.content_type =="product_created":
        product=Product(id=data["id"],title=data["title"],image=data["image"])
        db.session.add(product)
        db.session.commit()
        print("Product Created")
    elif properties.content_type =="product_updated":
        product=Product.query.get(data["id"])
        product.title=data["title"]
        product.image=data["image"]
        db.session.commit()
        print("Product updated")
    elif properties.content_type =="product_deleted":
        product= Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print("Product deleted")

channel.basic_consume(queue="main",on_message_callback=callback,auto_ack=True)

print("\nStarted consuming\n")

channel.start_consuming()

channel.close()
