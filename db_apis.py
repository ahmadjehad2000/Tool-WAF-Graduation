from extensions import db
from datetime import datetime
import time
import re


def remove_internals(d):

    return {k: v for (k, v) in d.items() if not k.startswith("_")}


def get_all_hosts():

    hosts = {host["hostname"]: remove_internals(
        host) for host in db.hosts.find()}
    return hosts


def get_host(hostname):

    host = db.hosts.find_one({"hostname": hostname})
    return remove_internals(host)


def set_host(host):

    existing_host = db.hosts.find_one({"hostname": host["hostname"]})
    if not existing_host:
        db.hosts.insert_one(host)
    else:
        db.hosts.update_one({"hostname": host["hostname"]}, {"$set": host})


def getCapture():
    captures = {capture["id"]: remove_internals(
        capture) for capture in db.captures.find()}
    return captures


def setCapture(capture):
    existing_cap = db.hosts.find_one({"id": capture["id"]})
    if not existing_cap:
        db.captures.insert_one(capture)
    else:
        db.captures.insert_one(capture)


def getBlockingIP(target, token):
    max_wait = 100
    start_time = datetime.now()
    while(datetime.now() - start_time).total_seconds() < max_wait:
        blocking = db.blocking.find_one({"target": target, "token": token})
        if not blocking:
            time.sleep(5)
            continue
        return remove_internals(blocking)
    return {}


def get_portscan(target, token):

    max_wait_time = 300  # extended port scan allowed to take 5 minutes max
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < max_wait_time:

        # print(f"searching db for target: {target}, token: {token}")
        scan = db.portscans.find_one({"target": target, "token": token})
        if not scan:
            time.sleep(5)
            continue

        # print(f"found it, returning scan: {scan}")
        return remove_internals(scan)

    return {}  # portscan results never found


def get_traceroute(target, token):

    max_wait_time = 300  # extended port scan allowed to take 5 minutes max
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < max_wait_time:

        # print(f"searching db for target: {target}, token: {token}")
        traceroute = db.traceroutes.find_one(
            {"target": target, "token": token})
        if not traceroute:
            time.sleep(5)
            continue

        # print(f"found it, returning traceroute: {traceroute}")
        return remove_internals(traceroute)

    return {}  # traceroute results never found


def getDevice():

    devices = {device['device_name']: remove_internals(
        device) for device in db.devices.find()}
    return devices


def setDevice(device):

    db.devices.insert_one(device)


def record_blocking_data(blocking_data):
    db.blocking.insert_one(blocking_data)


def record_portscan_data(portscan_data):

    db.portscans.insert_one(portscan_data)


def record_traceroute_data(traceroute_data):

    db.traceroutes.insert_one(traceroute_data)
