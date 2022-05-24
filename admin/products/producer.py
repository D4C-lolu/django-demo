import pika,json


params=pika.URLParameters("amqps://udrtfoht:eUowJnkHLUKeQC2VG-w25KD3T3xWOF8r@beaver.rmq.cloudamqp.com/udrtfoht")

connection = pika.BlockingConnection(params)

channel= connection.channel()

def publish(method,body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange="",routing_key="main",body=json.dumps(body), properties=properties)
    