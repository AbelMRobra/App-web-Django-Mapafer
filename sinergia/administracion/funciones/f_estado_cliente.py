import datetime
from administracion.models import CuotasPrestamo, Pagos, Prestamos, Clientes

def eliminar_cuotas_prestamo(prestamo):

    cuotas_prestamo = CuotasPrestamo.objects.filter(prestamo = prestamo)
    
    for cuota in cuotas_prestamo:
        cuota.delete()

def crear_cuotas_prestamo(prestamo):

    prestamo = Prestamos.objects.get(id = prestamo.id)

    pagos_list = Pagos.objects.filter(prestamo = prestamo).values_list("monto", flat = True)
    fecha_primer_pago = datetime.date(prestamo.primera_cuota.year, prestamo.primera_cuota.month, prestamo.primera_cuota.day)
    pagos = sum(pagos_list)
    pagado_auxiliar = pagos
    
    if prestamo.regimen == "QUINCENAL":
        cuotas_pasadas = 0
        fecha_aux = fecha_primer_pago
        while cuotas_pasadas < prestamo.cuotas:
            cuotas_pasadas +=1

            if len(CuotasPrestamo.objects.filter(prestamo = prestamo, fecha = fecha_aux)) == 0:

                cuota_nueva = CuotasPrestamo(
                    prestamo = prestamo,
                    fecha =  fecha_aux,
                    numero = cuotas_pasadas,
                    monto = prestamo.monto/prestamo.cuotas,
                    
                )
                cuota_nueva.save()
            else:
                cuota_nueva = CuotasPrestamo.objects.get(prestamo = prestamo, fecha = fecha_aux)
                cuota_nueva.numero = cuotas_pasadas
                cuota_nueva.save()

            if pagado_auxiliar >= cuota_nueva.monto:
                cuota_nueva.estado = "SI"
            elif pagado_auxiliar > 0:
                cuota_nueva.estado = "PARCIAL"
            else:
                cuota_nueva.estado = "NO"
            cuota_nueva.save()
            pagado_auxiliar -= cuota_nueva.monto

            fecha_aux = fecha_aux + datetime.timedelta(days=15)


    if prestamo.regimen == "MENSUAL":
        cuotas_pasadas = 0
        fecha_aux = fecha_primer_pago
        while cuotas_pasadas < prestamo.cuotas:
            cuotas_pasadas +=1

            if len(CuotasPrestamo.objects.filter(prestamo = prestamo, fecha = fecha_aux)) == 0:

                cuota_nueva = CuotasPrestamo(
                    prestamo = prestamo,
                    fecha =  fecha_aux,
                    numero = cuotas_pasadas,
                    monto = prestamo.monto/prestamo.cuotas,
                    
                )
                cuota_nueva.save()
            else:
                cuota_nueva = CuotasPrestamo.objects.get(prestamo = prestamo, fecha = fecha_aux)
                cuota_nueva.numero = cuotas_pasadas
                cuota_nueva.save()

            if pagado_auxiliar >= cuota_nueva.monto:
                cuota_nueva.estado = "SI"
            elif pagado_auxiliar > 0:
                cuota_nueva.estado = "PARCIAL"
            else:
                cuota_nueva.estado = "NO"
            cuota_nueva.save()
            pagado_auxiliar -= cuota_nueva.monto

            if fecha_aux.month != 12:
                    fecha_aux = datetime.date(fecha_aux.year, fecha_aux.month +1, fecha_aux.day)
            else:
                fecha_aux = datetime.date(fecha_aux.year + 1, 1, fecha_aux.day)

def calcular_estado(cliente):

    if cliente.estado != "Rechazado":

        prestamos = Prestamos.objects.filter(cliente = cliente)

        nivel_deuda = []

        for prestamo in prestamos:

            mora_total = calcular_mora(prestamo)

            valor_cuota = prestamo.monto/prestamo.cuotas

            if mora_total/valor_cuota <= 1:
                nivel_deuda.append(1)

            elif mora_total/valor_cuota <= 3:
                nivel_deuda.append(2)
            elif mora_total/valor_cuota <= 6:
                nivel_deuda.append(3)
            elif mora_total/valor_cuota <= 12:
                nivel_deuda.append(4)
            elif mora_total/valor_cuota > 12:
                nivel_deuda.append(5)
            else:
                nivel_deuda.append(6)

    return mora