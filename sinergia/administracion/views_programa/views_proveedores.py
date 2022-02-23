from django.shortcuts import render, redirect
from administracion.models import Prestamos, Proveedor, PagosProveedores
from ..funciones.f_proveedores import *
import numpy as np

def proveedor_panel(request):

    context = {}

    if request.method == 'POST':

        context["mensaje"] = proveedores_borrar(request.POST['id_proveedor'])

    proveedores_refresh_deuda()
    context['proveedores'] = proveedores_calculo_deuda()

    return render(request, "proveedores/proveedor_panel.html", context)

def proveedor_agregar(request):

    context = {}

    if request.method == 'POST':

        context["mensaje"] = proveedores_agregar(request.POST['razon_social'], request.POST['fantasia'])


    return render(request, "proveedores/proveedor_agregar.html", context)

def proveedor_editar(request, id_proveedor):

    context = {}

    if request.method == 'POST':

        context['mensaje'] = proveedores_editar(id_proveedor, request.POST['razon_social'], request.POST['fantasia'])

    # Información para render

    context["proveedor"] = Proveedor.objects.get(id = id_proveedor)

    return render(request, "proveedores/proveedores_editar.html", context)

def proveedor_pagos(request, id_proveedor):
    proveedor = Proveedor.objects.get(id = id_proveedor)
    context = {}

    if request.method == 'POST':

        try:
            context['mensaje'] = proveedores_borrar_pagos(request.POST['id_pago_borrar'])

        except:

            try:
                context['mensaje'] = proveedores_editar_pagos(request.POST['id_pago'], request.POST['id_deuda'], request.POST['fecha'], request.POST['monto'])
                

            except:
                context['mensaje'] = proveedores_agregar_pagos(proveedor,request.POST['id_deuda'], request.POST['fecha'], request.POST['monto'])

    # Información para render

    context['pagos'] = PagosProveedores.objects.filter(proveedor= proveedor).order_by("-fecha")
    context['proveedor'] = proveedor
    context['deudas'] = proveedores_deuda_info(proveedor)

    return render(request, "proveedores/proveedor_pagos.html", context)