import pika
import json
from datetime import datetime


def start_blocking(target):
    print(f"Start blocking process for {target}")
    token = str(datetime.now())
    blocking_info = {
        "waf": "localhost:5000",
        "work_type": "blocking",
        "target": target,
        "token": token,
    }
    blocking_info_json = json.dumps(blocking_info)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="waf", durable=True)
    channel.basic_publish(
        exchange="", routing_key="waf", body=blocking_info_json
    )
    return token


if __name__ == "__main__":
    start_blocking("192.168.1.11")
