from .models import Prestamos, Pagos, Clientes
import numpy as np

def montos_situaciones():

    con_prestamos = Prestamos.objects.all()
    con_pagos = Pagos.objects.all()

    context = {}
    context["situacion_1"] = sum(np.array(con_prestamos.filter(cliente__estado = "Situación 1").values_list("monto", flat=True))) - sum(np.array(con_pagos.filter(prestamo__cliente__estado = "Situación 1").values_list("monto", flat=True)))
    context["situacion_2"] = sum(np.array(con_prestamos.filter(cliente__estado = "Situación 2").values_list("monto", flat=True))) - sum(np.array(con_pagos.filter(prestamo__cliente__estado = "Situación 2").values_list("monto", flat=True)))
    context["situacion_3"] = sum(np.array(con_prestamos.filter(cliente__estado = "Situación 3").values_list("monto", flat=True))) - sum(np.array(con_pagos.filter(prestamo__cliente__estado = "Situación 3").values_list("monto", flat=True)))
    context["situacion_4"] = sum(np.array(con_prestamos.filter(cliente__estado = "Situación 4").values_list("monto", flat=True))) - sum(np.array(con_pagos.filter(prestamo__cliente__estado = "Situación 4").values_list("monto", flat=True)))
    context["situacion_5"] = sum(np.array(con_prestamos.filter(cliente__estado = "Situación 5").values_list("monto", flat=True))) - sum(np.array(con_pagos.filter(prestamo__cliente__estado = "Situación 5").values_list("monto", flat=True)))
    context["situacion_6"] = sum(np.array(con_prestamos.filter(cliente__estado = "Situación 6").values_list("monto", flat=True))) - sum(np.array(con_pagos.filter(prestamo__cliente__estado = "Situación 6").values_list("monto", flat=True)))

    return context

def cantidad_situaciones():

    context = {}
    context["user_1"] = len(Clientes.objects.filter(estado = "Situación 1"))
    context["user_2"] = len(Clientes.objects.filter(estado = "Situación 2"))
    context["user_3"] = len(Clientes.objects.filter(estado = "Situación 3"))
    context["user_4"] = len(Clientes.objects.filter(estado = "Situación 4"))
    context["user_5"] = len(Clientes.objects.filter(estado = "Situación 5"))
    context["user_6"] = len(Clientes.objects.filter(estado = "Situación 6"))

    return context