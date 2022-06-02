
from tabulate import tabulate
import requests
import json


def defineDevices():
    name = input('enter device name: ')
    type = input('enter device type: ')
    host = input('enter ip: ')
    user = input('enter user: ')
    passwd = input('enter pass: ')
    device = {
        "device_name": name,
        "device_type": type,
        "host": host,
        "username": user,
        "password": passwd
    }
    return device


def updateDevice():
    jsonObj = defineDevices()
    rsp = requests.put("http://127.0.0.1:5000/devices", json=jsonObj)
    if rsp.status_code != 204:
        print("Error updating devices via REST API")
    else:
        print("successfully updated devices via REST API")


# def printDevices():
#     jsonobj = requests.get("http://127.0.0.1:5000/devices")
#     if jsonobj.status_code != 200:
#         print("Error getting devices via REST API")
#     else:
#         devices = jsonobj.json()
#         for i in devices:
#             print(i)
#             print(tabulate([devices[i]['device_name']],
#                   [devices[i]['device_name']], [devices[i]['host']], [devices[i]['username']], [devices[i]['password']]))
#             print("\n")


if __name__ == "__main__":
    updateDevice()
