#!/usr/bin/python3

import requests
import datetime
import os
import logging
import functools
import time
import json
from requests.auth import HTTPDigestAuth
import concurrent.futures

BASEDIR = "/var/backups/cams"
LOGLEVEL = logging.INFO
CAMERA_IP = ["192.168.100.20", "192.168.100.21", "192.168.100.23"]
CAMERA_USER = ""
CAMERA_PASS = ""

def debug_wrap(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug(f"Entering Function {func.__name__} {args} {kwargs}")
        output = func(*args, **kwargs)
        logging.debug(f"Exiting Function {func.__name__}")
        return output
    return wrapper


@debug_wrap
def mkdir(dir):
    path = dir.split("/")
    for p in range(1, len(path) + 1):
        try:
            d = "/".join(path[:p])
            os.stat(d)
            logging.debug(f"{d} Exists")
        except FileNotFoundError:
            logging.debug(f"{d} Creating")
            try:
                os.mkdir(d)
            except OSError:
                logging.debug(f"{d} Creation Failed")


@debug_wrap
def backup(camera, user, pwd, logdir):
    try:
        logging.info(f"Retrieveing Backup for {camera}")
        r = requests.get(f"http://{camera}/cgi-bin/Config.backup?action=All",
                     auth=HTTPDigestAuth(user, pwd),
                     timeout=30)
        with open(f"{logdir}/{camera}.txt", "w") as f:
            f.write(json.dumps(r.json(), indent=2))
            logging.info(f"Writing Backup for {camera} to {logdir}/{camera}.txt")
    except Exception as e:
        logging.info(f"Connection Failed {e}")
    time.sleep(2)


if __name__ == '__main__':
    if LOGLEVEL == logging.DEBUG:
        logging.basicConfig(level=LOGLEVEL,
                        format='%(asctime)s - (%(threadName)-30s) - %(levelname)10s - %(message)s')
    else:
        logging.basicConfig(level=LOGLEVEL,
                            format='%(asctime)s - %(message)s')
    logdir = f'{BASEDIR}/{datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")}'
    mkdir(logdir)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        for cam in CAMERA_IP:
            executor.submit(backup, *[cam, CAMERA_USER, CAMERA_PASS, logdir])
