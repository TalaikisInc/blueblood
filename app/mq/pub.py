from .conn import channel


def main(e, key, msg):
    connection, _channel = channel()
    _channel.basic_publish(exchange=e, routing_key=key, body=msg)
    connection.close()
