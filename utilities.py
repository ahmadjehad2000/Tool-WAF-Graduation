from datetime import datetime
import requests
from pprint import pformat, pprint


def send_blocking(source, destination, target, token, timestamp, blocking_output):
    blocking_payload = {
        "source": source,
        "target": target,
        "token": token,
        "timestamp": timestamp,
        "blocking_output": pformat(blocking_output),
    }
    rsp = requests.post(
        "http://" + destination + "/workerbroker/blocking", json=blocking_payload
    )
    if rsp.status_code != 204:
        print(
            f"{str(datetime.now())[:-3]}: Error calling /blocking/store response: {rsp.status_code}, {rsp.content}"
        )
    else:
        print(f"{str(datetime.now())[:-3]}: Blocking sent")
    return rsp.status_code
