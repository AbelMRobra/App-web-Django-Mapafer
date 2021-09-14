from django.shortcuts import render, redirect
from administracion.models import Citas, Clientes, Prestamos, Pagos, Proveedor, Empresa, CuotasPrestamo
import numpy_financial as npf
import numpy as np
from ..funciones.f_estado_cliente import *

def prestamos_panel(request):

    if request.method == 'POST':
        
        prestamo_a_borrar = Prestamos.objects.get(id = int(request.POST['borrar']))
        cliente =prestamo_a_borrar.cliente
        prestamo_a_borrar.delete()
        cliente.estado = estado_cliente(cliente)
        cliente.save()

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
    return render(request, "prestamos/prestamo_panel.html", {'data':data})

def prestamos_agregar(request):

    clientes = Clientes.objects.all()
    proveedores = Proveedor.objects.all()
    formulario = 0
    context = {}

    if request.method == 'POST':

        try:
            string_cliente = request.POST['cliente'].split("-")
            string_proveedor = request.POST['proveedor'].split("-")
            
            cliente = Clientes.objects.get(id = string_cliente[0])
            
            new_credito = Prestamos(
                cliente = cliente,
                proveedor = Proveedor.objects.get(id = string_proveedor[0]),
                fecha = request.POST['fecha'],
                primera_cuota = request.POST['priimeracuota'],
                valor_original = request.POST['precio1'],
                presupuesto_cliente = request.POST['precio3'],
                monto = request.POST['precio2'],
                cuotas = int(request.POST['cuotas']),
                regimen = request.POST['regimen'],
            )
            new_credito.save()

            cliente.estado = estado_cliente(cliente)
            cliente.save()

            
            formulario = 0
            context["mensaje"] = 1


            try:
                new_credito.adjunto = request.FILES['adjunto']
                new_credito.save()
            except:
                pass

        except:

            monto_inicial = float(request.POST['monto'])
            regimen = request.POST['regimen']
            cantidad_cuotas = float(request.POST['cuotas'])

            if regimen == "QUINCENAL":
                cantidad_cuotas = cantidad_cuotas/2
            
            tasa_anual = float(request.POST['tasa'])
            
            tasa_mensual = float((1 + tasa_anual/100))
            tasa_mensual = tasa_mensual**0.0833333333333333-1
            importe_cuota = npf.pmt(tasa_mensual, cantidad_cuotas, -monto_inicial,)
            monto_prestamo = importe_cuota*cantidad_cuotas

            if regimen == "QUINCENAL":

                importe_cuota = importe_cuota/2
                cantidad_cuotas = cantidad_cuotas*2

            formulario = 1
            context["monto"] = monto_prestamo
            context["monto_base"] = monto_inicial
            context["cuota"] = int(cantidad_cuotas)
            context["regimen"] = regimen

    context["clientes"] = clientes
    context["proveedores"] = proveedores
    context["formulario"] = formulario
        
    return render(request, "prestamos/calculadora.html", context)

def prestamos_detalle_completo(request, id_credito):

    credito = Prestamos.objects.get(id = id_credito)

    if request.method == 'POST':
        
        id_proveedor = request.POST['proveedor'].split("-")[0]
        proveedor = Proveedor.objects.get(id = int(id_proveedor))
        credito.proveedor = proveedor
        credito.valor_original = request.POST['valor_original']
        credito.monto = request.POST['monto']
        credito.cuotas = request.POST['cuotas']
        credito.presupuesto_cliente = request.POST['presupuesto_cliente']
        credito.fecha = request.POST['fecha']
        credito.save()

        if request.POST['primera_cuota'] != str(credito.primera_cuota):
            cuotas_prestamo = CuotasPrestamo.objects.filter(prestamo = credito)
            for c in cuotas_prestamo:
                c.delete()
            credito.primera_cuota = request.POST['primera_cuota']
            credito.save()

        return redirect('Administrar credito', id_credito = credito.id)


    cuotas = CuotasPrestamo.objects.filter(prestamo = credito)

    pagos = Pagos.objects.filter(prestamo = credito)

    total_pagado = sum(Pagos.objects.filter(prestamo = credito).values_list("monto", flat=True))

    proveedores = Proveedor.objects.all()

    context = {}
    context['credito'] = credito
    context['cuotas'] = cuotas
    context['pagos'] = pagos
    context['total_pagado'] = total_pagado
    context['proveedores'] = proveedores

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
