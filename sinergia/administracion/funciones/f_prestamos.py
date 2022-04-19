import numpy_financial as npf
import numpy as np
from administracion.models import Prestamos
from ..funciones.f_estado_cliente import *
from django.db.models import Q

def prestamos_validacion_cuotas():
    cuotas_validar = CuotasPrestamo.objects.filter(Q(monto_interes = None)|Q(monto_bonificado = None))

    for cuota in cuotas_validar:
        if cuota.monto_interes == None:
            cuota.monto_interes = 0
            cuota.save()

        if cuota.monto_bonificado == None:
            cuota.monto_bonificado = 0
            cuota.save()

def prestamos_validar_anomalias():
    query_prestamos = Prestamos.objects.all()
    query_cuotas = CuotasPrestamo.objects.all()
    query_pagos = Pagos.objects.all()

    for prestamo in query_prestamos:
        print(prestamo)


def prestamos_cuotas_pagos(id_prestamo):
    prestamo = Prestamos.objects.get(id = id_prestamo)
    cuotas = CuotasPrestamo.objects.filter(prestamo = prestamo)
    pagos = sum(np.array(Pagos.objects.filter(prestamo = prestamo).values_list("monto", flat=True)))
    monto_prestamo = sum(np.array(cuotas.monto) + np.array(cuotas.monto_interes) - np.array(cuotas.monto_bonificado))
    saldo = monto_prestamo - pagos

    for cuota in cuotas:
        if saldo < 20:
            cuota.estado = "SI"
        else:
            monto_cuota = cuota.monto + cuota.monto_interes - cuota.monto_bonificado

            if pagos > int(monto_cuota):
                cuota.estado = "SI"
                pagos -= int(monto_cuota)

            elif (int(monto_cuota) - pagos) < 5:
                cuota.estado = "SI"
                pagos = 0

            elif pagos > 5:
                cuota.estado = "PARCIAL"
                pagos = 0
            
            else:
                cuota.estado = "NO"
            
        cuota.save()

def prestamos_agregar_credito(cliente, proveedor, fecha, primera_cuota, 
    valor_original, presupuesto_cliente, monto, cuotas, 
    regimen, monto_valor_actual=0):

    try:
        prestamo_nuevo = Prestamos(
            cliente = cliente,
            proveedor = proveedor,
            fecha = fecha,
            primera_cuota = primera_cuota,
            valor_original = valor_original,
            valor_actual_ar = monto_valor_actual,
            presupuesto_cliente = presupuesto_cliente,
            monto = monto,
            cuotas = cuotas,
            regimen = regimen,
        )
        prestamo_nuevo.save()

        crear_cuotas_prestamo(prestamo_nuevo)
        return ([1, "Prestamo agregado correctamente"], prestamo_nuevo.id)

    except:
        return ([0, "Ocurrio un error inesperado"],)

def prestamos_adjuntar_archivo(id_prestamo, adjunto):

    prestamo_a_modificar = Prestamos.objects.get(id = id_prestamo)
    prestamo_a_modificar.adjunto = adjunto
    prestamo_a_modificar.save()

    return [1, "Prestamo y adjunto agregado correctamente"]

def prestamos_editar_credito(id_credito, proveedor, fecha, primera_cuota, valor_original, presupuesto_cliente, monto, cuotas):

    try:

        credito = Prestamos.objects.get(id = id_credito)

        primera_cuota_original = credito.primera_cuota

        credito.proveedor = proveedor
        credito.valor_original = valor_original
        credito.monto = monto
        credito.cuotas = cuotas
        credito.presupuesto_cliente = presupuesto_cliente
        credito.fecha = fecha
        credito.primera_cuota = primera_cuota
        credito.save()

        if primera_cuota_original != credito.primera_cuota:
            
            eliminar_cuotas_prestamo(credito)

        # estado_cliente(credito.cliente)

        return [1, "Prestamo editado correctamente"]

    except:

        return [0, "Ocurrio un error inesperado"]

def prestamos_borrar_prestamo(id_prestamo):

    try:

        prestamo_a_borrar = Prestamos.objects.get(id = id_prestamo)
        
        cliente =prestamo_a_borrar.cliente
        
        prestamo_a_borrar.delete()
        
        # estado_cliente(cliente)

        return [1, "Prestamo borrado correctamente"]

    except:

        return [0, "Ocurrio un error inesperado"]

def prestamos_calculadora(tasa, monto_inicial, periodo_gracia, regimen, cantidad_cuotas):
    tasa_anual = float(tasa)/100

    if regimen == "QUINCENAL":
        tasa_ajustada = (1 + tasa_anual)**(1/24) - 1

    else:
        tasa_ajustada = (1 + tasa_anual)**(1/12) - 1

    if periodo_gracia > 0:
        monto_ajustado = -monto_inicial*(1+tasa_ajustada)**(periodo_gracia)

    else:
        monto_ajustado = -monto_inicial

    importe_cuota = npf.pmt(tasa_ajustada, cantidad_cuotas, monto_ajustado,)
    monto_prestamo = importe_cuota*cantidad_cuotas
    return [round(monto_prestamo, 2), round(importe_cuota, 2), int(cantidad_cuotas)]

def prestamos_refinanciaminto_calculo(id_prestamo, tasa_deuda, tasa_saldo):
    prestamo = Prestamos.objects.get(id = id_prestamo)
    cuotas = CuotasPrestamo.objects.filter(prestamo = prestamo).exclude(estado = "SI")

    monto_deuda_actual = 0
    monto_deuda_historica = 0
    cuotas_deuda = 0
    monto_saldo_actual = 0
    monto_saldo_historica = 0
    cuotas_saldo = 0

    hoy = datetime.date.today()

    for cuota in cuotas:

        if cuota.fecha < hoy:
            tasa = tasa_deuda/100
            tasa_ajustada = (1 + tasa)**(1/365) - 1
            dias = (hoy - cuota.fecha).days
        
        else:
            tasa = tasa_saldo/100
            tasa_ajustada = (1 + tasa)**(1/365) - 1
            dias = (hoy - cuota.fecha).days

        monto = cuota.monto 
        monto_ajustado = npf.fv(tasa_ajustada, dias, 0, -monto)

        if cuota.fecha < hoy:
            monto_deuda_historica += cuota.monto 
            monto_deuda_actual += monto_ajustado
            cuotas_deuda += 1

        else:
            monto_saldo_historica += cuota.monto  
            monto_saldo_actual += monto_ajustado
            cuotas_saldo += 1

    return {"DeudaHistorica": round(monto_deuda_historica, 0), "SaldoHistorica": round(monto_saldo_historica, 0), "DeudaActual": round(monto_deuda_actual, 0), "SaldoActual": round(monto_saldo_actual, 0), "CantidadDeuda": cuotas_deuda, "CantidadSaldo": cuotas_saldo}

def prestamos_cancelar_refinanciamiento(id_prestamo, tasa_deuda, tasa_saldo):

    prestamo = Prestamos.objects.get(id = id_prestamo)
    cliente = prestamo.cliente

    cuotas = CuotasPrestamo.objects.filter(prestamo = prestamo).exclude(estado = "SI")

    monto_deuda_actual = 0
    monto_saldo_actual = 0

    hoy = datetime.date.today()

    for cuota in cuotas:

        if cuota.fecha < hoy:

            tasa = tasa_deuda/100
            tasa_ajustada = (1 + tasa)**(1/365) - 1
            dias = (hoy - cuota.fecha).days
        
        else:

            tasa = tasa_saldo/100
            tasa_ajustada = (1 + tasa)**(1/365) - 1
            dias = (hoy - cuota.fecha).days


        monto = cuota.monto 
        monto_ajustado = npf.fv(tasa_ajustada, dias, 0, -monto)

        if cuota.fecha < hoy:
            cuota.monto_interes = monto_ajustado - cuota.monto 
            cuota.estado = "SI"
            cuota.save()

            monto_deuda_actual += monto_ajustado
  

        else:
            cuota.monto_bonificado = monto_ajustado - cuota.monto 
            cuota.estado = "SI"
            cuota.save() 
            
            monto_saldo_actual += monto_ajustado

    pago_final = Pagos(

        comentarios = "Refinanciamiento por nuevo credito",
        prestamo = prestamo,
        fecha = hoy,
        monto = (monto_deuda_actual + monto_saldo_actual)
    )

    # estado_cliente(cliente)
    pago_final.save()

def simular_cuotas_prestamo(regimen, cantidad_cuotas, primer_pago):

    fecha_primer_pago = datetime.date(int(primer_pago[0:4]), int(primer_pago[5:7]), int(primer_pago[8:10]))
    fechas =  []
    
    if regimen == "QUINCENAL":
        cuotas_pasadas = 0
        fecha_aux = fecha_primer_pago
        while cuotas_pasadas < cantidad_cuotas:
            cuotas_pasadas +=1
            fechas.append(fecha_aux)
            fecha_aux = fecha_aux + datetime.timedelta(days=15)


    if regimen == "MENSUAL":
        cuotas_pasadas = 0
        fecha_aux = fecha_primer_pago
        while cuotas_pasadas < cantidad_cuotas:
            cuotas_pasadas +=1
            fechas.append(fecha_aux)
            if fecha_aux.month != 12:
                    fecha_aux = datetime.date(fecha_aux.year, fecha_aux.month +1, fecha_aux.day)
            else:
                fecha_aux = datetime.date(fecha_aux.year + 1, 1, fecha_aux.day)

    return fechas