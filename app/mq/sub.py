from retry import retry

from pika.exceptions import AMQPConnectionError

from .conn import channel


@retry(AMQPConnectionError, delay=5, jitter=(1, 3))
def main(key):
    connection, _channel = channel()
    for method_frame, properties, body in _channel.consume(key):
        # print(method_frame, properties, body)
        _channel.basic_ack(method_frame.delivery_tag)

        if method_frame.delivery_tag == 10:
            break

    requeued_messages = _channel.cancel()
    print('Requeued %i messages' % requeued_messages)
    connection.close()
