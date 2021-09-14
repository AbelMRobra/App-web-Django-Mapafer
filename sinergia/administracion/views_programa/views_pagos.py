from django.shortcuts import render, redirect
from administracion.models import Pagos, Prestamos
from ..funciones.f_estado_cliente import *

def pagos_panel(request):

    if request.method == 'POST':
        
        consulta_borrar = Pagos.objects.get(id = int(request.POST['borrar']))
        cliente = consulta_borrar.prestamo.cliente
        consulta_borrar.delete()
        cliente.estado = estado_cliente(cliente)
        cliente.save()

    context = {}
    context['pagos'] = Pagos.objects.all().order_by("-fecha")
    context['prestamos'] = Prestamos.objects.all().order_by("cliente__apellido")
    
    return render(request, 'pagos/panelpagos.html', context)

def pagos_agregar(request, id_prestamo):

    if request.method == 'POST':
        new_pago = Pagos(
            prestamo = Prestamos.objects.get(id = int(request.POST['prestamo'].split("-")[0])),
            monto = request.POST['monto'],
            fecha = request.POST['fecha']
        )
        new_pago.save()
        
        cliente = new_pago.prestamo.cliente
        cliente.estado = estado_cliente(cliente)
        cliente.save()
        
        return redirect('Panel de pagos')

    context = {}
    if id_prestamo == "0":
        context['id_prestamo'] = 0
    else:
        context['id_prestamo'] = Prestamos.objects.get(id = int(id_prestamo))
        context['valor_cuota'] = round(context['id_prestamo'].monto/context['id_prestamo'].cuotas, 2)
    
    context['pagos'] = Pagos.objects.all()
    context['prestamos'] = Prestamos.objects.all().order_by("cliente__apellido")
    
    return render(request, 'pagos/agregarpagos.html', context)

def pagos_editar(request, id_pago):

    pago = Pagos.objects.get(id = id_pago)

    if request.method == 'POST':

        pago.prestamo = Prestamos.objects.get(id = int(request.POST['prestamo'].split("-")[0]))
        pago.monto = request.POST['monto']
        pago.fecha = request.POST['fecha']
        pago.save()

        cliente = pago.prestamo.cliente
        cliente.estado = estado_cliente(cliente)
        cliente.save()
        
        return redirect('Panel de pagos')

    context = {}
    
    context['pago'] = pago
    context['pagos'] = Pagos.objects.all()
    context['prestamos'] = Prestamos.objects.all().order_by("cliente__apellido")
    
    return render(request, 'pagos/editarpagos.html', context)