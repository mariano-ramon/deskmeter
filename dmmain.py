import subprocess
import os
import datetime
import time

from pymongo import MongoClient
from pprint import pprint

client = MongoClient()

now = datetime.datetime.utcnow

db = client.deskmeter
switches = db.switch
dailies = db.daily

desktops = ("Work",
            "Browse",
            "Write",
            "Learn",
            "Idle")


unlabeled = "Other"

def active_workspace():

    workspaces = subprocess.check_output(["wmctrl", "-d"]) \
                           .decode("utf-8").strip("\n").split("\n")

    for workspace in workspaces:
        if workspace[3] == "*":
            return int(workspace[0])


def desktop(workspace_index):
    try:
        return desktops[workspace_index]
    except IndexError:
        return unlabeled



current_workspace = active_workspace()
last_switch_time = now()

while True:
    if current_workspace != active_workspace():

        delta = round((now() - last_switch_time ).total_seconds())
        switch = {  "workspace": desktop(current_workspace),
                    "date": last_switch_time,
                    "delta": delta }
        
        switches.insert_one(switch)
        current_workspace = active_workspace()
        last_switch_time = now()

    time.sleep(1)