#!/usr/bin/python3

import requests
import pytz
import datetime
from requests.auth import HTTPDigestAuth
from dateutil import parser

local_tz = pytz.timezone('America/New_York')


API = "https://api.sunrise-sunset.org/json"
LAT = "37.60"
LNG = "-79.60"
DELTA = datetime.timedelta(minutes=45)
CAMERA_IP = ["192.168.100.10", "192.168.100.11"]
CAMERA_USER = ""
CAMERA_PASS = ""

###
try:
    r = requests.get(f"{API}?lat={LAT}&lng={LNG}")
except Exception as e:
    print(f"Unable to retrieve JSON Sunrise {e}")
    quit()

sunrise = pytz.utc.localize(parser.parse(r.json()['results']['sunrise'])).astimezone()
sunset = pytz.utc.localize(parser.parse(r.json()['results']['sunset'])).astimezone()

timesection = (sunrise + DELTA) .strftime("%H:%M:%S") + "-" + (sunset - DELTA) .strftime("%H:%M:%S")

for c in CAMERA_IP:
    url = f"http://{c}/cgi-bin/configManager.cgi?action=setConfig&VideoInMode[0].TimeSection[0][0]=1%20{timesection}"
    try:
        r = requests.get(url, auth=HTTPDigestAuth(CAMERA_USER, CAMERA_PASS), timeout=5)
        print(f"Updating Camera {c} {timesection}")
        r.raise_for_status()
    except Exception as e:
        print(f"Unable to update Camera {c} {timesection} {e}")
