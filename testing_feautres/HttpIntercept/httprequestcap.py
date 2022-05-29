
import json
import uuid
from time import sleep
import requests
from scapy.all import *
from scapy.layers.http import HTTPRequest
from tabulate import tabulate
from datetime import time


def sniff_scapy(iface=None):
    if iface:
        # port 80 for http (generally)
        # `process_packet` is the callback
        sniff(filter="port 80", prn=process_packet, iface=iface, store=False)
    else:
        # sniff with default interface
        sniff(filter="port 80", prn=process_packet, store=False)


def process_packet(packet):
    if packet.haslayer(HTTPRequest):
        url = packet[HTTPRequest].Host.decode(
        ) + packet[HTTPRequest].Path.decode()
        httpver = packet[HTTPRequest].Http_Version.decode()
        ip = packet[IP].src
        destip = packet[IP].dst
        method = packet[HTTPRequest].Method.decode()
        nowdate = datetime.now()
        currentdate = nowdate.strftime("%d/%m/%Y")
        currenttime = nowdate.strftime("%H:%M:%S")
        id = str(uuid.uuid4().fields[-1])[:5]
        packetinfo = [packet]
        print(tabulate({"ID": [id], "SRC": [ip], "DST": [destip],
                        "Method": [method, httpver], "URL": [url], "Timestamp": [currenttime, currentdate], "packet": [packetinfo]}, headers="keys"))
        capture = {
            "id": id,
            "srcip": ip,
            "dstip": destip,
            "method": method,
            "httpver": httpver,
            "url": url,
            "timestamp": [currentdate, currenttime],
            "full-packet-info": str(packetinfo)
        }

        updatecap(capture)


def updatecap(capture):
    rsp = requests.put("http://127.0.0.1:5000/capture", json=capture)
    if rsp.status_code != 204:
        print(
            f"Error updating capture via REST API capture info:\n SourceIP:{capture['srcip']}\n URL:{capture['url']}\n Timestamp:{capture['timestamp']}")
    else:
        print(
            f"successfully post the capture via REST API info SourceIP:{capture['srcip']} DestIP:{capture['dstip']} URL:{capture['url']}")


def getcap():
    print("Retriving old captures")
    rsp = requests.get("http://127.0.0.1:5000/capture")
    if rsp.status_code != 200:
        print(f"Error getting captures via REST API {rsp.reason}")
        return {}
    else:
        print("Captures retrieved succsefully")
        return rsp.json()


def printcap():
    rsp = requests.get("http://127.0.0.1:5000/capture")
    if rsp.status_code != 200:
        print(f"Error getting captures via REST API {rsp.reason}")
        return {}
    else:
        print("Captures retrieved succsefully")
        with open("packetcapture.json", mode='w') as file:
            packetinfo = str(rsp.json())
            file.write(packetinfo)


if __name__ == "__main__":
    try:
        sniff_scapy("wlx503eaa283690")
    except KeyboardInterrupt:
        print("shutting down")
        exit()
    finally:
        printcap()
        sleep(3)
        print("shutting down")
