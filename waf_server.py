from tracemalloc import start
from waf_server_utils import fix_target
from flask_cors import CORS
from db_apis import getDevice, setDevice
from db_apis import get_all_hosts, set_host, get_portscan
from db_apis import getCapture, setCapture
from db_apis import getBlockingIP, record_blocking_data
from flask import Flask, request
from rabbitMQ_worker_api import start_blocking

waf_app = Flask(__name__)
CORS(waf_app)


@waf_app.route("/hosts", methods=["GET", "PUT"])
def hosts():

    if request.method == "GET":
        return get_all_hosts()

    elif request.method == "PUT":
        hostname = request.args.get("hostname")
        if not hostname:
            return "must provide hostname on PUT", 400

        host = request.get_json()
        set_host(host)
        return {}, 204


@waf_app.route("/devices", methods=["GET", "PUT"])
def devices():
    if request.method == "GET":
        return getDevice()
    elif request.method == "PUT":
        devices = request.get_json()
        setDevice(devices)
        return {}, 204


@waf_app.route("/capture", methods=["GET", "PUT"])
def capture():
    if request.method == "GET":
        return getCapture()
    elif request.method == "PUT":
        capture = request.get_json()
        setCapture(capture)
        return {}, 204


# @quokka_app.route("/scan", methods=["GET", "POST"])
# def scan_endpoint():
#     target = request.args.get("target")
#     if not target:
#         return "must provide target to get portscan", 400
#     if request.method == "GET":
#         token = request.args.get("token")
#         if not token:
#             return "must provide token to get portscan", 400
#         return get_portscan(target, token)
#     elif request.method == "POST":
#         token = start_portscan(target)
#         return {"token": token}


@waf_app.route("/blocking", methods=["GET", "POST"])
def blockbasedIP():
    target = request.args.get("target")
    if not target:
        return "Must provide target", 400
    if request.method == "GET":
        token = request.args.get("token")
        if not token:
            return "Must provide token to get the blocking service", 400
        return getBlockingIP(target, token)
    elif request.method == "POST":
        token = start_blocking(target)
        return {"token": token}


@waf_app.route("/workerbroker/blocking", methods=["POST"])
def workerBlocking():
    blocking_data = request.get_json()
    record_blocking_data(blocking_data)
    return {}, 204


# @quokka_app.route("/worker/portscan", methods=["POST"])
# def worker_portscan_endpoint():
#     portscan_data = request.get_json()
#     record_portscan_data(portscan_data)
#     return {}, 204


if __name__ == "__main__":
    waf_app.run()
