from pika import BlockingConnection, ConnectionParameters, exceptions


def channel(multi=False):
    while(True):
        try:
            if multi:
                config = (
                    ConnectionParameters(host='rabbitmq.zone1.domain.com', connection_attempts=5, retry_delay=1),
                    ConnectionParameters(host='rabbitmq.zone2.domain.com', connection_attempts=5, retry_delay=1)
                )
                connection = BlockingConnection(config)
            else:
                connection = BlockingConnection()
            return connection, connection.channel()
        except exceptions.ConnectionClosedByBroker:
            break
        except exceptions.AMQPChannelError:
            break
        except exceptions.AMQPConnectionError:
            continue
