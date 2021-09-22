from django.shortcuts import render, redirect
from administracion.models import Citas, Clientes, Prestamos, Pagos, Proveedor, Empresa, CuotasPrestamo
import numpy_financial as npf
import numpy as np
from ..funciones.f_estado_cliente import *
from ..funciones.f_prestamos import *

def prestamos_panel(request):

    context = {}

    if request.method == 'POST':

        context["mensaje"] = prestamos_borrar_prestamo(int(request.POST['borrar']))

    data = []

    data_aux = Prestamos.objects.all()

    for d in data_aux:
        today = datetime.date.today()
        pagos_list = Pagos.objects.filter(prestamo = d).values_list("monto", flat = True)

        if d.monto != 0:
            avance = sum(np.array(pagos_list))/d.monto*100
        else:
            avance = 100

        cant = len(pagos_list)
        pagos = sum(pagos_list)
        saldo = d.monto - pagos    
        fecha_prestamo = datetime.date(d.fecha.year, d.fecha.month, d.fecha.day)
        fecha_primer_pago = datetime.date(d.primera_cuota.year, d.primera_cuota.month, d.primera_cuota.day)
        if d.regimen == "QUINCENAL":
            cuotas_pasadas = 0
            fecha_aux = fecha_primer_pago
            while fecha_aux < today:
                cuotas_pasadas +=1
                if cuotas_pasadas == d.cuotas:
                    break
                else:
                    fecha_aux = fecha_aux + datetime.timedelta(days=15)
            mora = cuotas_pasadas*(d.monto/d.cuotas) - pagos

            prox_vencimiento = fecha_aux 
            data.append((d, pagos, saldo, prox_vencimiento, mora, avance))
        
        if d.regimen == "MENSUAL":
            cuotas_pasadas = 0
            fecha_aux = fecha_primer_pago
            while fecha_aux < today:
                cuotas_pasadas +=1
                if cuotas_pasadas == d.cuotas:
                    break
                else:
                    if fecha_aux.month != 12:
                        fecha_aux = datetime.date(fecha_aux.year, fecha_aux.month +1, fecha_aux.day)
                    else:
                        fecha_aux = datetime.date(fecha_aux.year + 1, 1, fecha_aux.day)
            mora = cuotas_pasadas*(d.monto/d.cuotas) - pagos

            prox_vencimiento = fecha_aux 
            data.append((d, pagos, saldo, prox_vencimiento, mora, avance))

    context["data"] = data
    return render(request, "prestamos/prestamo_panel.html", context)

def prestamos_agregar(request):

    estado_del_calculo = 0
    
    context = {}

    if request.method == 'POST':

        try:

            string_cliente = request.POST['cliente'].split("-")
            string_proveedor = request.POST['proveedor'].split("-")
            cliente = Clientes.objects.get(id = string_cliente[0])
            proveedor = Proveedor.objects.get(id = string_proveedor[0])

            context["mensaje"] = prestamos_agregar_credito(cliente, proveedor, request.POST['fecha'], 
            request.POST['priimeracuota'], request.POST['precio1'], request.POST['precio3'], 
            request.POST['precio2'], int(request.POST['cuotas']), request.POST['regimen'])

            try:
                context["mensaje"] = prestamos_adjuntar_archivo(context["mensaje"][1], request.FILES['adjunto'])

            except:
                context["mensaje"] = context["mensaje"][0]


            estado_del_calculo = 0

            cliente.estado = estado_cliente(cliente)
            cliente.save()

        except:

            monto_inicial = float(request.POST['monto'])
            regimen = request.POST['regimen']
            cantidad_cuotas = float(request.POST['cuotas'])
            
            datos_calculadora = prestamos_calculadora(request.POST['tasa'], monto_inicial, regimen, cantidad_cuotas)

            estado_del_calculo = 1
            context["monto"] = datos_calculadora[0]
            context["monto_cuota"] = datos_calculadora[1]
            context["monto_base"] = monto_inicial
            context["cuota"] = datos_calculadora[2]
            context["regimen"] = regimen

    context["clientes"] = Clientes.objects.all()
    context["proveedores"] = Proveedor.objects.all()
    context["estado_del_calculo"] = estado_del_calculo
        
    return render(request, "prestamos/prestamo_agregar.html", context)

def prestamos_detalle_completo(request, id_credito):

    context = {}

    credito = Prestamos.objects.get(id = id_credito)

    context['credito'] = credito

    if request.method == 'POST':
        
        id_proveedor = request.POST['proveedor'].split("-")[0]
        proveedor = Proveedor.objects.get(id = int(id_proveedor))

        context["mensaje"] = prestamos_editar_credito(id_credito, proveedor, request.POST['fecha'], 
        request.POST['primera_cuota'], request.POST['valor_original'], request.POST['presupuesto_cliente'], 
        request.POST['monto'], request.POST['cuotas'])

        context['credito'] = Prestamos.objects.get(id = id_credito)


        
    context['cuotas'] = CuotasPrestamo.objects.filter(prestamo = credito)
    context['pagos'] = Pagos.objects.filter(prestamo = credito)
    context['total_pagado'] = sum(Pagos.objects.filter(prestamo = credito).values_list("monto", flat=True))
    context['proveedores'] = Proveedor.objects.all()

    return render(request, 'prestamos/prestamo_detalle.html', context)

def prestamos_informacion(request):

    data = []

    data_aux = Prestamos.objects.all()

    for d in data_aux:
        interes = (d.monto/d.valor_original - 1)*100
        pagos = sum(Pagos.objects.filter(prestamo = d).values_list("monto", flat = True))
        avance = pagos/d.monto*100
        cuota = d.monto/d.cuotas
        tae = (interes/d.cuotas)*12
        aux = 1/360
        tna = (((1+tae)**aux)-1)*360
        data.append((d, interes, avance, cuota, tae, tna))

    return render(request, "prestamos/informacion.html", {'data':data})
