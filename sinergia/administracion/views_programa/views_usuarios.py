from django.shortcuts import render
import requests
import pandas as pd
import json


def usuarios_panel(request):

    return render(request, "usuarios/usuarios_principal.html")

