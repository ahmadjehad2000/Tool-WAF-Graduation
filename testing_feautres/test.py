from pprint import pprint

import subprocess

command = "ping -c3"
target = "192.168.1.11"
blocking_output = subprocess.check_output(
    ["iptables", "-I", "INPUT", "-s", target, "-j", "DROP"])
print(blocking_output)
