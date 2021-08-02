from django.shortcuts import render, redirect
from .models import Prestamos, Proveedor, PagosProveedores
import numpy as np

def panel_proveedores(request):

    proveedores = Proveedor.objects.all()

    data_proveedores = []

    for proveedor in proveedores:
        prestamos_asociados = len(Prestamos.objects.filter(proveedor = proveedor))
        monto_prestado = sum(np.array(Prestamos.objects.filter(proveedor = proveedor).values_list("valor_original", flat=True)))
        pagado = 0
        saldo = monto_prestado - pagado
        data_proveedores.append((proveedor, prestamos_asociados, monto_prestado, pagado, saldo))

    context = {}
    context['proveedores'] = data_proveedores



    return render(request, "proveedores/panel_proveedores.html", context)

def newproveedor(request):

    mensaje = 0

    if request.method == 'POST':

        b = Proveedor(
            razon_social = request.POST['razon_social'],
            fantasia = request.POST['fantasia'],
        )

        b.save()

        return redirect('Panel proveedor')

    return render(request, "proveedores/new_proveedores.html", {"mensaje":mensaje})

def editarproveedor(request, id_proveedor):

    proveedor = Proveedor.objects.get(id = id_proveedor)

    if request.method == 'POST':

        proveedor.razon_social = request.POST['razon_social']
        proveedor.fantasia = request.POST['fantasia']
        proveedor.save()

        return redirect('Panel proveedor')

    context = {}
    context["proveedor"] = proveedor

    return render(request, "proveedores/editar_proveedor.html", context)

def pagosproveedor(request, id_proveedor):

    context = {}

    return render(request, "proveedores/pago_proveedor.html", context)