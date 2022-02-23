from datetime import *
from dateutil.relativedelta import *
import numpy as np
from administracion.models import Proveedor, DeudaProveedor, PagosProveedores, Prestamos

def proveedores_refresh_deuda():
    
    proveedores = Proveedor.objects.all()
    prestamos = Prestamos.objects.all()

    for proveedor in proveedores:

        prestamos_proveedor = prestamos.filter(proveedor = proveedor)

        for prestamo in prestamos_proveedor:

            if len(DeudaProveedor.objects.filter(prestamo = prestamo)) == 0:
                 
                nueva_deuda = DeudaProveedor(
                     prestamo = prestamo,
                     fecha = (prestamo.primera_cuota + timedelta(days=30)),
                )
                
                nueva_deuda.save()

def proveedores_calculo_deuda():

    proveedores = Proveedor.objects.all()

    proveedor_datos = []

    for proveedor in proveedores:
        
        prestamos_asociados = len(Prestamos.objects.filter(proveedor = proveedor))
        
        monto_prestado = sum(np.array(DeudaProveedor.objects.filter(prestamo__proveedor = proveedor).values_list("prestamo__valor_original", flat=True)))
        pagado = sum(np.array(PagosProveedores.objects.filter(proveedor= proveedor).values_list("monto", flat=True)))
        saldo = monto_prestado - pagado
        proveedor_datos.append((proveedor, prestamos_asociados, monto_prestado, pagado, saldo))

    return proveedor_datos

def proveedores_deuda_info(proveedor):
    deudas = DeudaProveedor.objects.filter(prestamo__proveedor = proveedor).order_by("fecha")
    info_deudas = []

    for deuda in deudas:
        pagos = sum(np.array(PagosProveedores.objects.filter(deuda = deuda).values_list("monto", flat=True)))
        
        if deuda.prestamo.valor_original != 0:
            avance = pagos/deuda.prestamo.valor_original*100
        else:
            avance = 100

        saldo = round((1 - avance)*deuda.prestamo.valor_original, 2)

        info_deudas.append((deuda, avance, saldo))

    return info_deudas

def chequeo_deuda_pagada(id_deuda):
    deuda = DeudaProveedor.objects.get(id = id_deuda)
    pagos = sum(np.array(PagosProveedores.objects.filter(deuda = deuda).values_list("monto", flat=True)))

    if pagos >= deuda.prestamo.valor_original:
        deuda.estado_pagado = True
        deuda.save()

    else:
        deuda.estado_pagado = False
        deuda.save()

def proveedores_agregar_pagos(proveedor, id_deuda, fecha, monto):

    try:
        nuevo_pago = PagosProveedores(
            proveedor = proveedor,
            deuda = DeudaProveedor.objects.get(id = id_deuda),
            fecha = fecha,
            monto = monto

        )
        nuevo_pago.save()

        chequeo_deuda_pagada(id_deuda)

        return [1, "Pago cargado correctamente"]

    except:

        return [0, "Ocurrio un error inesperado"]

def proveedores_editar_pagos(id_pago, id_deuda, fecha, monto):

    try:
        pago_a_editar = PagosProveedores.objects.get(id = id_pago)
        pago_a_editar.deuda = DeudaProveedor.objects.get(id = id_deuda)
        pago_a_editar.fecha = fecha
        pago_a_editar.monto = monto
        pago_a_editar.save()

        chequeo_deuda_pagada(id_deuda)

        return [1, "Pago editado correctamente"]

    except:

        return [0, "Ocurrio un error inesperado"]

def proveedores_borrar_pagos(id_pago):

    try:
        pago_a_borrar = PagosProveedores.objects.get(id = id_pago)
        if pago_a_borrar.deuda:
            id_deuda = pago_a_borrar.deuda.id
        else:
            id_deuda = 0
        
        pago_a_borrar.delete()

        if id_deuda:
            chequeo_deuda_pagada(id_deuda)

        return [1, "Pago borrado correctamente"]

    except:

        return [0, "Ocurrio un error inesperado"]

def proveedores_borrar(id_proveedor):

    try:
        proveedor_a_borrar = Proveedor.objects.get(id = id_proveedor)
        proveedor_a_borrar.delete()

        return [1, "Proveedor eliminado correctamente"]

    except:

        return [0, "Ocurrio un error inesperado"]

def proveedores_editar(id_proveedor, razon_social, fantasia):

    try:

        proveedor = Proveedor.objects.get(id = id_proveedor)
        proveedor.razon_social = razon_social
        proveedor.fantasia = fantasia
        proveedor.save()

        return [1, "Proveedor editado correctamente"]

    except:

        return [0, "Ocurrio un error inesperado"]

def proveedores_agregar(razon_social, fantasia):

    try:

        nuevo_proveedor = Proveedor(
            razon_social = razon_social,
            fantasia = fantasia
        )

        nuevo_proveedor.save()

        return [1, "Proveedor agregado correctamente"]

    except:

        return [0, "Ocurrio un error inesperado"]



    