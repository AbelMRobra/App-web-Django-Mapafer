from django.shortcuts import render, redirect
from administracion.models import Pagos, Prestamos
from ..funciones.f_estado_cliente import *
from ..funciones.f_prestamos import prestamos_cuotas_pagos

def pagos_panel(request):
    if request.method == 'POST':
        consulta_borrar = Pagos.objects.get(id = int(request.POST['borrar']))
        cliente = consulta_borrar.prestamo.cliente
        consulta_borrar.delete()

    context = {}
    context['pagos'] = Pagos.objects.all().order_by("-fecha")
    context['prestamos'] = Prestamos.objects.all().order_by("cliente__apellido")
    return render(request, 'pagos/panelpagos.html', context)

def pagos_agregar(request, id_prestamo):

    if request.method == 'POST':
        prestamo = Prestamos.objects.get(id = int(request.POST['prestamo'].split("-")[0]))
        new_pago = Pagos(
            prestamo = prestamo,
            monto = request.POST['monto'],
            fecha = request.POST['fecha']
        )
        new_pago.save()
        prestamos_cuotas_pagos(prestamo.id)
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
        prestamo = Prestamos.objects.get(id = int(request.POST['prestamo'].split("-")[0]))
        pago.prestamo = prestamo
        pago.monto = request.POST['monto']
        pago.fecha = request.POST['fecha']
        pago.save()

        prestamos_cuotas_pagos(prestamo.id)
        
        return redirect('Panel de pagos')

    context = {}
    context['pago'] = pago
    context['pagos'] = Pagos.objects.all()
    context['prestamos'] = Prestamos.objects.all().order_by("cliente__apellido")
    
    return render(request, 'pagos/editarpagos.html', context)

def pagos_user(request):
    context = {}
    context['pagos'] = Pagos.objects.filter(prestamo__cliente__usuario__user = request.user.id).order_by("-fecha")
    return render(request, 'pagos/pagos_user.html', context)
