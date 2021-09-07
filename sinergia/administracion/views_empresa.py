from django.shortcuts import render, redirect
from .models import Empresa, Clientes, Pagos, CuotasPrestamo
import datetime
from datetime import timedelta
from .google_sheet import programa_social_empresa

def perfilempresa(request, id_empresa):

    context = {}
    context['programa'] = programa_social_empresa(id_empresa)
    context['empresa'] = Empresa.objects.get(id = id_empresa)
    context['clientes'] = Clientes.objects.filter(empresa__id = id_empresa).order_by("apellido").exclude(estado = "Potencial")

    return render(request, "empresa/perfil_empresa.html", context)

def panelempresas(request):

    context = {}

    hoy = datetime.date.today()

    if hoy.day < 13:
        dia_auxiliar_1 = datetime.date(hoy.year, hoy.month, 1)
        dia_auxiliar_2 = dia_auxiliar_1 - timedelta(days = 5)
        dia_auxiliar_3 = dia_auxiliar_1 + timedelta(days = 5)

    else:
        dia_auxiliar_1 = datetime.date(hoy.year, hoy.month, 15)
        dia_auxiliar_2 = dia_auxiliar_1 - timedelta(days = 5)
        dia_auxiliar_3 = dia_auxiliar_1 + timedelta(days = 5)

    if request.method == 'POST':

        try:

            try:
                empresa_editar = Empresa.objects.get(id =request.POST["id"] )
                empresa_editar.nombre = request.POST["nombre"]
                empresa_editar.save()
                context['mensaje'] = "Empresa editada exitosamente"
                    
            except:

                new_empresa = Empresa(
                    nombre = request.POST["nombre"]
                    )
                new_empresa.save()
                context['mensaje'] = "Empresa creada exitosamente"

        except:

            context['mensaje_error'] = "Surgio un error inesperado"

    
    context["empresas"] = Empresa.objects.all()
    
    datos_completos = []

    for empresa in context["empresas"]:
        clientes = len(Clientes.objects.filter(empresa = empresa))
        cant_cuotas = len(CuotasPrestamo.objects.filter(prestamo__cliente__empresa= empresa, fecha__range = (dia_auxiliar_2, dia_auxiliar_3)).order_by("prestamo__cliente__apellido").exclude(estado = "SI"))
        monto_ven = sum(CuotasPrestamo.objects.filter(prestamo__cliente__empresa= empresa, fecha__range = (dia_auxiliar_2, dia_auxiliar_3)).exclude(estado = "SI").values_list("monto", flat = True))

        datos_completos.append((empresa, clientes, cant_cuotas, monto_ven))

    context["informacion"] = datos_completos

    return render(request, "empresa/panel_empresa.html", context)

def panel_pagos(request, id_empresa):

    empresa = Empresa.objects.get(id = id_empresa)

    hoy = datetime.date.today()

    if hoy.day < 13:
        dia_auxiliar_1 = datetime.date(hoy.year, hoy.month, 1)
        dia_auxiliar_2 = dia_auxiliar_1 - timedelta(days = 5)
        dia_auxiliar_3 = dia_auxiliar_1 + timedelta(days = 5)

    else:
        dia_auxiliar_1 = datetime.date(hoy.year, hoy.month, 15)
        dia_auxiliar_2 = dia_auxiliar_1 - timedelta(days = 5)
        dia_auxiliar_3 = dia_auxiliar_1 + timedelta(days = 5)

    if request.method == 'POST':

        try:
            dia_auxiliar_2 = request.POST["fecha_desde"]
            dia_auxiliar_3 = request.POST["fecha_hasta"]

        except:


            data = request.POST.items()

            for d in data:
                if "cuota" in d[0]:
                    cuota = CuotasPrestamo.objects.get(id = d[1])
                    new_pago = Pagos(
                        prestamo = cuota.prestamo,
                        fecha = hoy,
                        monto = cuota.monto,
                    )

                    new_pago.save()

                    cuota.estado = "SI"
                    cuota.save()
    
    
    data_filtrada = CuotasPrestamo.objects.filter(prestamo__cliente__empresa__id = id_empresa, fecha__range = (dia_auxiliar_2, dia_auxiliar_3)).order_by("prestamo__cliente__apellido").exclude(estado = "SI")
    
    context = {}
    context["data"] = data_filtrada
    context["empresa"] = empresa
    context["fecha_1"] = dia_auxiliar_2
    context["fecha_2"] = dia_auxiliar_3
    
    return render(request, "empresa/panel_pagos.html", context)