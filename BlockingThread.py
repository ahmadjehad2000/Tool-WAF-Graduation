import subprocess
from threading import Thread
from datetime import datetime
from utilities import send_blocking
from socket import gethostname


class BlockingThread(Thread):
    def __init__(self, destination, blocking_info):
        super().__init__()
        print(
            f"BlockingThread: initializing thread object: blocking_info={blocking_info}")
        if "target" not in blocking_info:
            print(
                f"BlockingThread: missing information in blocking_info: {blocking_info}")
            return
        self.destination = destination
        self.target = blocking_info["target"]
        self.token = blocking_info["token"]
        self.commandarg = "ping -c3"

    def process_blocking(self, blocking_output):
        status_code = send_blocking(
            gethostname(),
            self.destination,
            self.target,
            self.token,
            str(datetime.now())[:-1],
            blocking_output,
        )
        print(f"\nBlockingThread: blocking sent, result={status_code}\n")

    def run(self):
        print(f"Starting Blocking thread for {self.target}")
        print(f"Executing command {self.commandarg} {self.target}")
        blocking_output = subprocess.check_output(
            ["iptables", "-I", "INPUT", "-s", self.target, "-j", "DROP"])
        blocking_output = str(blocking_output.decode('utf-8')+"Blocking")
        if blocking_output is None:
            print(f"BlockingThread: blocking failed for {self.target}")
            return
        else:
            print(f"BlockingThread: blocking succeeded for {self.target}")
        # iptables -I INPUT -s 192.168.1.100 -j DROP
            self.process_blocking(
                blocking_output)
        print(f"Completed Blocking thread for {self.target}")
