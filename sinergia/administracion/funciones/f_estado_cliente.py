import datetime
from administracion.models import CuotasPrestamo, Pagos, Prestamos


def armar_cuotas(prestamo):

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

def estado_cliente(cliente):
    
    today = datetime.date.today()
    prestamos_cliente = Prestamos.objects.filter(cliente = cliente)
    estados = []
    if len(prestamos_cliente) > 0:
        for prestamo in prestamos_cliente:
            armar_cuotas(prestamo)
            cuotas = CuotasPrestamo.objects.filter(prestamo = prestamo).order_by("fecha").exclude(estado = "SI")
            if len(cuotas) == 0:
                estados.append(0)
            else:
                dif_dias = (today - cuotas[0].fecha).days

                if dif_dias < 31:
                    estados.append(1)
                elif dif_dias < 90:
                    estados.append(2)
                elif dif_dias < 180:
                    estados.append(3)
                elif dif_dias < 365:
                    estados.append(4)
                else:
                    estados.append(5)
        estados.sort(reverse=True)
        estado_cliente = estados[0]
        if estado_cliente == 0:
            estado_cliente = "No activo"
        if estado_cliente == 1:
            estado_cliente = "Situación 1"
        if estado_cliente == 2:
            estado_cliente = "Situación 2"
        if estado_cliente == 3:
            estado_cliente = "Situación 3"
        if estado_cliente == 4:
            estado_cliente = "Situación 4"
        if estado_cliente == 5:
            estado_cliente = "Situación 5"

        
    else:
        estado_cliente = "Potencial"

    return estado_cliente

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