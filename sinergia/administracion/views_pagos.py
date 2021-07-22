from django.shortcuts import render, redirect
from .models import Pagos, Prestamos

def pagos_panel(request):
    context = {}
    context['pagos'] = Pagos.objects.all()
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
        return redirect('Panel de pagos')

    context = {}
    if id_prestamo == "0":
        context['id_prestamo'] = 0
    else:
        context['id_prestamo'] = Prestamos.objects.get(id = int(id_prestamo))
    context['pagos'] = Pagos.objects.all()
    context['prestamos'] = Prestamos.objects.all().order_by("cliente__apellido")
    return render(request, 'pagos/agregarpagos.html', context)