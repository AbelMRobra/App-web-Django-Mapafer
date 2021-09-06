import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings
from .models import Empresa, Clientes

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

def programa_social_empresa(id_empresa):

    # Conexión a Google para tener la información

    ruta_clave = settings.MEDIA_ROOT + '/claves/mapafer-323416-24b701a8563c.json'
    scope = ['https://spreadsheets.google.com/feeds', "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name(ruta_clave, scope)

    client = gspread.authorize(creds)

    sheet = client.open("Mapafer-Respuestas").sheet1

    sheet_pandas = pd.DataFrame(sheet.get_all_records())

    # Preguntas

    context = {}

    context['preguntas'] = [pregunta for pregunta in sheet_pandas.columns if "?" in pregunta] 
    clientes_empresa = Clientes.objects.filter(empresa__id = id_empresa)

    data = []

    count = 0
    for pregunta in context['preguntas']:

        respuestas = []
        tipo_list = []

        n = 1
        for cliente in clientes_empresa:

            mask = sheet_pandas['Dirección de correo electrónico'] == cliente.email
            sheet_filter = sheet_pandas[mask]
            if sheet_filter.shape[0] != 0:
                max_value = sheet_pandas.index[mask].tolist()
                data_columna = sheet_filter[mask].loc[max_value[-1], pregunta]
                if data_columna != "":

                    if type(data_columna) == "str":
                        tipo = 0
                        respuestas.append(data_columna)
                    else:
                        tipo = 1
                        respuestas.append((n, data_columna))
                        n += 1

                    tipo_list.append(tipo)

        cuantos = len(respuestas)
        tipo = sum(tipo_list)
        count += 1
        
        data.append((count, pregunta, tipo, cuantos, respuestas))

    print(data)

    return data


