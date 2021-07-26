from django.shortcuts import render, redirect
from .models import Proveedor

def panel_proveedores(request):

    context = {}
    context['proveedores'] = Proveedor.objects.all()

    return render(request, "proveedores/panel_proveedores.html", context)

def newproveedor(request):

    mensaje = 0

    if request.method == 'POST':

        b = Proveedor(
            razon_social = request.POST['razon_social'],
            fantasia = request.POST['fantasia'],
        )

        b.save()

        return redirect('Home')

    return render(request, "proveedores/new_proveedores.html", {"mensaje":mensaje})