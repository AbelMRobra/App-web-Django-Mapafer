from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz
from google.oauth2 import service_account
from googleapiclient.discovery import build

def crear_evento(inicio, final, nombre, descripcion):

    service_account_email = "mapafercalendar@mapafer-323416.iam.gserviceaccount.com"
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    ruta_clave = settings.MEDIA_ROOT + '/claves/mapafer-323416-24b701a8563c.json'
    credentials = service_account.Credentials.from_service_account_file(ruta_clave)
    scoped_credentials = credentials.with_scopes(SCOPES)


    def build_service():
        service = build("calendar", "v3", credentials=scoped_credentials)
        return service

    def create_event():
        service = build_service()

        start_datetime = datetime.now(tz=pytz.utc)
        event = (
            service.events()
            .insert(
                calendarId="msuv5umh0njmqt1o543iu319fc@group.calendar.google.com",
                body={

                    "summary": "{}".format(nombre),
                    "description": "{}".format(descripcion),
                    "start": {"dateTime": inicio},
                    "end": {"dateTime": final},
                },
            )
            .execute()
        )

    create_event()