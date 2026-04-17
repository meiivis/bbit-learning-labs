
from consumer_interface import mqConsumerInterface
import os
import pika

class mqConsumer(mqConsumerInterface):
    def __init__(
        self, binding_key: str, exchange_name: str, queue_name: str
    ) -> None:
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name

        self.setupRMQConnection()
    def setupRMQConnection(self) -> None:

        #connections
        conParams = pika.URLParameters(os.environ['AMQP_URL'])
        self.connection = pika.BlockingConnection(parameters=conParams)
        self.channel = self.connection.channel()
        #create queue
        self.channel.queue_declare(queue=self.queue_name)
        #create exchange
        self.exchange = self.channel.exchange_declare(exchange=self.exchange_name)
        #bind queue
        self.channel.queue_bind(
            queue= self.queue_name,
            routing_key= self.routing_key,
            exchange=self.exchange_name,
        )
        self.channel.basic_consume(
            self.queue_name, self.on_message_callback, auto_ack=False
        )

    #done
    def on_message_callback(
        self, channel, method_frame, header_frame, body
    ) -> None:
        
        self.channel.basic_ack(method_frame.delivery_tag, False)
        print('The message is contained in the body parameter variable')
        
    

    #done
    def startConsuming(self) -> None:
        print('[*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    #done
    def __del__(self) -> None:
        print('Closing RMQ connection on destruction')
        #close channel and connection
        self.channel.close()
        self.connection.close()


