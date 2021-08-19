from pprint import pprint
from django.conf import settings
from .Google import Create_Service, convert_to_RFC_datetime

def agendar_calendar(inicio, final, tema, descrip, email):

    CLIENT_SECRET_FILE = settings.MEDIA_ROOT + "/claves/client_secret.json"
    API_NAME = 'calendar'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    calendar_id = 'msuv5umh0njmqt1o543iu319fc@group.calendar.google.com'

    hours_adjustment = 0
    event_request_body = {
        "start" : {
            "dateTime" : convert_to_RFC_datetime(int(inicio[0:4]), int(inicio[5:7]), int(inicio[8:10]), int(inicio[11:13]) + hours_adjustment, int(inicio[14:16])),
            "timeZone": "America/Argentina/Tucuman"
        },
        "end" : {
            "dateTime" : convert_to_RFC_datetime(int(final[0:4]), int(final[5:7]), int(final[8:10]), int(final[11:13]) + hours_adjustment, int(final[14:16])),
            "timeZone": "America/Argentina/Tucuman"
        },
        "summary": "{}".format(tema),
        "description": "{}".format(descrip),
        "colorid": 5,
        "status": "confirmed",
        "transparency": "opaque",
        "visibility": "private",
        "location": "Tucuman",
        "attendees": [
            {
                "comment":"Agendado por Mapafer",
                "email": "{}".format(email),
                "responseStatus": "accepted"
            
            }
            
        ],

    }

    maxAttendees = 5
    sendNotification = True
    sendUpdate = "none"
    supportsAttachments = True

    response = service.events().insert(
        calendarId = calendar_id,
        maxAttendees = maxAttendees,
        sendNotifications = sendNotification,
        sendUpdates = sendUpdate,
        supportsAttachments = supportsAttachments,
        body = event_request_body
    ).execute()