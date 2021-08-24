import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings

def programa_social(email):

    ruta_clave = settings.MEDIA_ROOT + '/claves/mapafer-323416-24b701a8563c.json'
    scope = ['https://spreadsheets.google.com/feeds', "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(ruta_clave, scope)

    client = gspread.authorize(creds)

    sheet = client.open("Mapafer-Respuestas").sheet1

    sheet_pandas = pd.DataFrame(sheet.get_all_records())

    try:
        mask = sheet_pandas['Dirección de correo electrónico'] == email
        sheet_filter = sheet_pandas[mask]
        columns = sheet_pandas.columns
        max_value = sheet_pandas.index[mask].tolist()
        data_columna = [(column, sheet_filter.loc[max_value[-1], column]) for column in columns]
    
    except:
        data_columna = []

    return data_columna
