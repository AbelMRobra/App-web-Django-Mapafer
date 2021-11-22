from django.shortcuts import render, redirect
from administracion.models import Citas, Clientes, Prestamos, Pagos, Proveedor, Empresa, CuotasPrestamo, TasaParaCreditos
import numpy_financial as npf
import numpy as np
from ..funciones.f_estado_cliente import *
from ..funciones.f_prestamos import *

def prestamos_panel(request):

    context = {}

    prestamos_validacion_cuotas()

    if request.method == 'POST':

        datos_post = request.POST.dict()

        if 'entregado_si' in datos_post:
            prestamo = Prestamos.objects.get(id = int(request.POST["entregado_si"]))
            prestamo.entregado = True
            prestamo.save()

        if 'entregado_no' in datos_post:
            prestamo = Prestamos.objects.get(id = int(request.POST["entregado_no"]))
            prestamo.entregado = False
            prestamo.save()

        if 'borrar' in datos_post:

            context["mensaje"] = prestamos_borrar_prestamo(int(request.POST['borrar']))

    data = []

    data_aux = Prestamos.objects.all()

    for d in data_aux:

        today = datetime.date.today()
        pagos_list = Pagos.objects.filter(prestamo = d).values_list("monto", flat = True)

        if d.monto != 0:
            avance = sum(np.array(pagos_list))/(d.monto + sum(CuotasPrestamo.objects.filter(prestamo = d).values_list("monto_interes", flat=True)) + sum(CuotasPrestamo.objects.filter(prestamo = d).values_list("monto_bonificado", flat=True)))*100
        else:
            avance = 100

        cant = len(pagos_list)
        
        pagos = sum(pagos_list)
        saldo = d.saldo_credito()   
        
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

def prestamos_credito_cargado(request, id_credito_nuevo, id_credito_anterior):

    context = {}
    context['credito_anterior'] = Prestamos.objects.get(id = int(id_credito_anterior))
    context['credito_nuevo'] = Prestamos.objects.get(id = int(id_credito_nuevo))

    return render(request, "prestamos/prestamo_credito_cargado.html", context)

def prestamos_agregar(request):

    estado_del_calculo = 0
    
    context = {}

    if request.method == 'POST':

        datos_post = request.POST.dict()

        if 'carga_tasa' in datos_post:
            try:
                if TasaParaCreditos.objects.filter(nombre = request.POST['nombre'], valor_tasa = request.POST['valor']).count() == 0:
                    nueva_tasa = TasaParaCreditos(
                        nombre = request.POST['nombre'],
                        valor_tasa = request.POST['valor'],
                    )

                    nueva_tasa.save()
                    context["mensaje"] = [1, "Tasa creada correctamente"]

                else:

                    context["mensaje"] = [0, "La tasa ya existe"]


            except:
                context["mensaje"] = [0, "Error al crear la tasa"]

        if 'calculo_inicial' in datos_post:

            try:

                    
                monto_inicial = float(request.POST['monto'])
                regimen = request.POST['regimen']
                cantidad_cuotas = float(request.POST['cuotas'])
                periodo_gracia = int(request.POST['periodo_gracia'])
                
                datos_calculadora = prestamos_calculadora(request.POST['tasa'], monto_inicial, periodo_gracia, regimen, cantidad_cuotas)

                estado_del_calculo = 1
                context["tasa_seleccionada"] = request.POST['tasa']
                context["monto"] = datos_calculadora[0]
                context["monto_cuota"] = datos_calculadora[1]
                context["monto_base"] = monto_inicial
                context["cuota"] = datos_calculadora[2]
                context["regimen"] = regimen

                context["mensaje"] = [1, "Calculo realizado correctamente"]

            except:

                context["mensaje"] = [0, "Error al calcular"]



        if 'calculo_final' in datos_post:

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

                # cliente.estado = estado_cliente(cliente)
                # cliente.save()

                context["mensaje"] = [1, "Credito generado correctamente"]

            except:

                context["mensaje"] = [0, "Error al calcular"]

            
    context["clientes"] = Clientes.objects.all()
    context["tasas"] = TasaParaCreditos.objects.all()
    context["proveedores"] = Proveedor.objects.all()
    context["estado_del_calculo"] = estado_del_calculo
        
    return render(request, "prestamos/prestamo_agregar.html", context)

def prestamos_refinanciar(request):

    context = {}
    context["paso_1"] = False
    context['creditos'] = Prestamos.objects.all().order_by("cliente__apellido")
    context["tasas"] = TasaParaCreditos.objects.all()

    if request.method == 'POST':

        datos_post = request.POST.dict()

        if 'paso_1' in datos_post:

            context['credito_seleccionado'] = Prestamos.objects.get(id = request.POST["credito"])
            context['tasa_deuda'] = TasaParaCreditos.objects.get(id = request.POST["tasa_deuda"])
            context['tasa_saldo'] = TasaParaCreditos.objects.get(id = request.POST["tasa_saldo"])

            datos_refinanciamiento = prestamos_refinanciaminto_calculo(request.POST["credito"], context['tasa_deuda'].valor_tasa, context['tasa_saldo'].valor_tasa)
            
            context['datos_refinanciamiento'] = datos_refinanciamiento
            context['total'] = round(datos_refinanciamiento["DeudaActual"] + datos_refinanciamiento["SaldoActual"], 0)


            context["paso_1"] = True
            context["paso_2"] = True

        if 'paso_3' in datos_post:

            context["paso_1"] = True
            context["paso_3"] = True

            context['credito_seleccionado'] = Prestamos.objects.get(id = request.POST["credito"])
            context['tasa_deuda'] = TasaParaCreditos.objects.get(id = request.POST["tasa_deuda"])
            context['tasa_saldo'] = TasaParaCreditos.objects.get(id = request.POST["tasa_saldo"])
            context["proveedores"] = Proveedor.objects.all()

            try:

                    
                monto_inicial = float(request.POST['monto'])
                regimen = request.POST['regimen']
                cantidad_cuotas = float(request.POST['cuotas'])
                periodo_gracia = int(request.POST['periodo_gracia'])
                id_tasa = int(float(request.POST["tasa"]))
                tasa = TasaParaCreditos.objects.get(id = id_tasa)
                
                datos_calculadora = prestamos_calculadora(tasa.valor_tasa, monto_inicial, periodo_gracia, regimen, cantidad_cuotas)

                context["tasa_seleccionada"] = tasa
                context["periodo_gracia"] = periodo_gracia
                context["monto"] = datos_calculadora[0]
                context["monto_cuota"] = datos_calculadora[1]
                context["monto_base"] = monto_inicial
                context["cuota"] = datos_calculadora[2]
                context["regimen"] = regimen

                context["mensaje"] = [1, "Calculo realizado correctamente"]

            except:

                context["mensaje"] = [0, "Error al calcular"]

        if 'calculo_final' in datos_post:

            try:

                context['tasa_deuda'] = TasaParaCreditos.objects.get(id = request.POST["tasa_deuda"])
                context['tasa_saldo'] = TasaParaCreditos.objects.get(id = request.POST["tasa_saldo"])
                string_cliente = request.POST['cliente'].split("-")
                string_proveedor = request.POST['proveedor'].split("-")
                cliente = Clientes.objects.get(id = string_cliente[0])
                proveedor = Proveedor.objects.get(id = string_proveedor[0])
                id_credito_anterior = int(request.POST["credito"])
                prestamos_cancelar_refinanciamiento(id_credito_anterior, context['tasa_deuda'].valor_tasa, context['tasa_saldo'].valor_tasa)
                context["mensaje"] = prestamos_agregar_credito(cliente, proveedor, request.POST['fecha'], 
                request.POST['priimeracuota'], request.POST['precio1'], request.POST['precio3'], 
                request.POST['precio2'], int(request.POST['cuotas']), request.POST['regimen'])

                id_credito = context["mensaje"][1]

                try:
                    context["mensaje"] = prestamos_adjuntar_archivo(context["mensaje"][1], request.FILES['adjunto'])

                except:
                    context["mensaje"] = context["mensaje"][0]


                # cliente.estado = estado_cliente(cliente)
                # cliente.save()

                return redirect('Cargado', id_credito_nuevo = id_credito, id_credito_anterior = id_credito_anterior)

            except:

                context["mensaje"] = [0, "Error al calcular"]

    return render(request, "prestamos/prestamo_recalculo_prestamo.html", context)

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


    context['cuotas_totales'] = CuotasPrestamo.objects.filter(prestamo = credito).count()
    context['cuotas_pagadas'] = CuotasPrestamo.objects.filter(prestamo = credito, estado = "SI").count()
    context['cuotas_vencidas'] = CuotasPrestamo.objects.filter(prestamo = credito, fecha__lt = datetime.date.today()).exclude(estado = "SI").count()
    context['cuotas_pendientes'] = CuotasPrestamo.objects.filter(prestamo = credito, fecha__gte = datetime.date.today() ).exclude(estado = "SI").count()
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
