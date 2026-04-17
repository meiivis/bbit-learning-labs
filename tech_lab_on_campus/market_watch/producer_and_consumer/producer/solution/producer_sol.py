


class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str) -> None:
        # Save the two variables needed to instantiate the class
        self.mqrouting_key = routing_key 
        self.mqexchange_name = exchange_name
        # Call the setupRMQConnection function.
        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        conParams = pika.URLParameters(os.environ['AMQP_URL'])
        self.connection = pika.BlockingConnection(parameters=conParams)

        # Establish Channel
        self.channel = self.connection.channel()

        # Create the exchange if not already present
        self.channel.exchange_declare(exchange=self.mqexchange_name)

    def publishOrder(self, message: str) -> None:
        # Publish a simple UTF-8 string message from the parameter.
        self.channel.basic_publish(exchange=self.mqexchange_name, routing=self.mqrouting_key, body=message)
        self.channel.close()
        self.connection.close()

    #def __del__(self) -> None:
        