#!/usr/bin/python3

import os
import requests

my_ip_file = os.path.join("/tmp", "myIp.txt")


def myIp():
    return requests.get("https://gianlu.dev/ip").text.strip()


def writToFile(filename, content):
    fp = open(filename, "wt", encoding="utf8")
    fp.write(content)
    fp.close()


def readFile(filename):
    fp = open(filename, "rt", encoding="utf8")
    content = fp.read().strip()
    fp.close()
    return content


if not os.path.exists(my_ip_file):
    writToFile(my_ip_file, "")

current_ip = myIp()
if current_ip != readFile(my_ip_file):
    print(current_ip, readFile(my_ip_file))
    writToFile(my_ip_file, current_ip)

    import Client
    Client.mainFunc()
