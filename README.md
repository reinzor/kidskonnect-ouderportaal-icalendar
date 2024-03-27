# kidskonnect-ouderportaal-icalendar

Create an iCalendar file (.ics, .ical) from the Kidskonnect ouderportaal agenda

# Requirements

- Python3

# Run

```
./kidskonnect-ouderportaal-icalendar.py --subdomain $SUBDOMAIN --username $USERNAME --password $PASSWORD calendar.ics
```

Example output `calendar.ics`:

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:kidskonnect-ouderportaal-icalendar
BEGIN:VEVENT
DTEND:20240108T114500Z
DTSTART:20240108T063000Z
SUMMARY:Kinderopvang $CHILD_FULLNAME
UID:5826fd45-d75b-4997-bb26-492ec1a174c6@5826.org
END:VEVENT
END:VCALENDAR
```
