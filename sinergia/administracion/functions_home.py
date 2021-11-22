from .models import Prestamos, Pagos, Clientes
import numpy as np

def montos_situaciones():

    con_prestamos = Prestamos.objects.all()
    con_pagos = Pagos.objects.all()

    context = {}
    context["situacion_1"] = sum(np.array([prestamo.monto for prestamo in con_prestamos if prestamo.cliente.estado_cliente() == "Situación 1"])) - sum(np.array([pago.monto for pago in con_pagos if pago.prestamo.cliente.estado_cliente() == "Situación 1"]))
    context["situacion_2"] = sum(np.array([prestamo.monto for prestamo in con_prestamos if prestamo.cliente.estado_cliente() == "Situación 2"])) - sum(np.array([pago.monto for pago in con_pagos if pago.prestamo.cliente.estado_cliente() == "Situación 2"]))
    context["situacion_3"] = sum(np.array([prestamo.monto for prestamo in con_prestamos if prestamo.cliente.estado_cliente() == "Situación 3"])) - sum(np.array([pago.monto for pago in con_pagos if pago.prestamo.cliente.estado_cliente() == "Situación 3"]))
    context["situacion_4"] = sum(np.array([prestamo.monto for prestamo in con_prestamos if prestamo.cliente.estado_cliente() == "Situación 4"])) - sum(np.array([pago.monto for pago in con_pagos if pago.prestamo.cliente.estado_cliente() == "Situación 4"]))
    context["situacion_5"] = sum(np.array([prestamo.monto for prestamo in con_prestamos if prestamo.cliente.estado_cliente() == "Situación 5"])) - sum(np.array([pago.monto for pago in con_pagos if pago.prestamo.cliente.estado_cliente() == "Situación 5"]))
    context["situacion_6"] = sum(np.array([prestamo.monto for prestamo in con_prestamos if prestamo.cliente.estado_cliente() == "Situación 6"])) - sum(np.array([pago.monto for pago in con_pagos if pago.prestamo.cliente.estado_cliente() == "Situación 6"]))

    return context

def cantidad_situaciones():

    con_clientes = Clientes.objects.all()

    context = {}

    context["user_datos_1"] = [cliente for cliente in con_clientes if cliente.estado_cliente() == "Situación 1"] 
    context["user_datos_2"] = [cliente for cliente in con_clientes if cliente.estado_cliente() == "Situación 2"] 
    context["user_datos_3"] = [cliente for cliente in con_clientes if cliente.estado_cliente() == "Situación 3"] 
    context["user_datos_4"] = [cliente for cliente in con_clientes if cliente.estado_cliente() == "Situación 4"] 
    context["user_datos_5"] = [cliente for cliente in con_clientes if cliente.estado_cliente() == "Situación 5"] 
    context["user_datos_6"] = [cliente for cliente in con_clientes if cliente.estado_cliente() == "Situación 6"] 
    
    context["user_1"] = len(context["user_datos_1"])
    context["user_2"] = len(context["user_datos_2"])
    context["user_3"] = len(context["user_datos_3"])
    context["user_4"] = len(context["user_datos_4"])
    context["user_5"] = len(context["user_datos_5"])
    context["user_6"] = len(context["user_datos_6"])
    
    

    return context