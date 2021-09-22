import numpy_financial as npf
from administracion.models import Prestamos
from ..funciones.f_estado_cliente import *

def prestamos_agregar_credito(cliente, proveedor, fecha, primera_cuota, valor_original, presupuesto_cliente, monto, cuotas, regimen):

    try:
        prestamo_nuevo = Prestamos(
            cliente = cliente,
            proveedor = proveedor,
            fecha = fecha,
            primera_cuota = primera_cuota,
            valor_original = valor_original,
            presupuesto_cliente = presupuesto_cliente,
            monto = monto,
            cuotas = cuotas,
            regimen = regimen,
        )
        prestamo_nuevo.save()

        estado_cliente(prestamo_nuevo.cliente)

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

        estado_cliente(credito.cliente)

        return [1, "Prestamo editado correctamente"]

    except:

        return [0, "Ocurrio un error inesperado"]

def prestamos_borrar_prestamo(id_prestamo):

    try:

        prestamo_a_borrar = Prestamos.objects.get(id = id_prestamo)
        
        cliente =prestamo_a_borrar.cliente
        
        prestamo_a_borrar.delete()
        
        estado_cliente(cliente)

        return [1, "Prestamo borrado correctamente"]

    except:

        return [0, "Ocurrio un error inesperado"]

def prestamos_calculadora(tasa, monto_inicial, regimen, cantidad_cuotas):

    if regimen == "QUINCENAL":
        cantidad_cuotas = cantidad_cuotas/2
    
    tasa_anual = float(tasa)
    
    tasa_mensual = float((1 + tasa_anual/100))
    tasa_mensual = tasa_mensual**0.0833333333333333-1
    importe_cuota = npf.pmt(tasa_mensual, cantidad_cuotas, -monto_inicial,)
    monto_prestamo = importe_cuota*cantidad_cuotas

    if regimen == "QUINCENAL":

        importe_cuota = importe_cuota/2
        cantidad_cuotas = cantidad_cuotas*2

    return [round(monto_prestamo, 2), round(importe_cuota, 2), int(cantidad_cuotas)]