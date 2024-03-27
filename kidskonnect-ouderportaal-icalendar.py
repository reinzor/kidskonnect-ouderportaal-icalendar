#!/usr/bin/env python3
#
# Copyright (c) 2024 Rein Appeldoorn
#

import argparse
from datetime import datetime, timedelta
from uuid import uuid4

import requests

parser = argparse.ArgumentParser(
    prog="Kidskonnect Ouderportaal iCalendar",
    description="Write an iCalendar file from the KidsKonnect Ouderportaal agenda",
)
parser.add_argument("--subdomain", required=True)
parser.add_argument("--username", required=True)
parser.add_argument("--password", required=True)
parser.add_argument("--days_delta", default=100)
parser.add_argument("filename", type=argparse.FileType("w"))
args = parser.parse_args()

login_response = requests.put(
    "https://{}.ouderportaal.nl/auth-api/login".format(args.subdomain),
    json={
        "username": args.username,
        "password": args.password,
    },
)
auth_token = login_response.json()["authToken"]

cookies = {
    "__Host-refresh_token": auth_token,
}

headers = {
    "Authorization": "Bearer {}".format(auth_token),
}

now = datetime.now()
from_date = (now - timedelta(days=args.days_delta)).strftime("%Y%m%d")
to_date = (now + timedelta(days=args.days_delta)).strftime("%Y%m%d")
agenda_response = requests.get(
    "https://{}.ouderportaal.nl/restservices-parent/calendar/{}/until/{}".format(
        args.subdomain, from_date, to_date
    ),
    cookies=cookies,
    headers=headers,
)

args.filename.write(
    """BEGIN:VCALENDAR
VERSION:2.0
PRODID:kidskonnect-ouderportaal-icalendar
"""
)

for day in agenda_response.json()["payload"]["days"]:
    for child in day["children"]:
        fullname = child["child"]["fullname"]
        for combined_planning_part in child["combinedPlanningParts"]:
            for planning_part in combined_planning_part["planningParts"]:
                SUMMARY = "Kinderopvang {}".format(fullname)
                DTSTART = datetime.utcfromtimestamp(
                    planning_part["startTime"] / 1000
                ).strftime("%Y%m%dT%H%M%SZ")
                DTEND = datetime.utcfromtimestamp(
                    planning_part["endTime"] / 1000
                ).strftime("%Y%m%dT%H%M%SZ")
                uid = str(uuid4())
                UID = "{}@{}.org".format(uid, uid[:4])
                args.filename.write(
                    """BEGIN:VEVENT
DTEND:{}
DTSTART:{}
SUMMARY:{}
UID:{}
END:VEVENT
""".format(
                        DTEND, DTSTART, SUMMARY, UID
                    )
                )

args.filename.write("END:VCALENDAR")
