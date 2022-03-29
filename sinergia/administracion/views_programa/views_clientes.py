import datetime
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from ..models import Citas, Clientes, Prestamos, Pagos, Proveedor, Empresa, CuotasPrestamo
from ..google_calendar import crear_evento
from ..google_sheet import programa_social
from ..funciones.f_estado_cliente import *

def clientes(request):

    if request.method == 'POST':

        # try:
        cliente = Clientes.objects.get(id = request.POST['borrar'])
        cliente.delete()
        
        # except:

        #     data = Clientes.objects.all().order_by("nombre")

        #     for d in data:

        #         cliente_Estado = estado_cliente(d)
        #         d.estado = cliente_Estado
        #         d.save()

    context = {}
    context["data"] = Clientes.objects.all().order_by("apellido")
    cons_prestamo = Prestamos.objects.all()

    for c in context["data"]:
        if len(cons_prestamo.filter(cliente = c)) == 0:
            c.estado = "Potencial"
            c.save()

    return render(request, "clientes/basededatosclientes.html", context)

def profileclient(request, id_cliente):

    context = {}
    context['data'] = Clientes.objects.get(id = id_cliente)
    context['programa_social'] = programa_social(context['data'].email)

    if request.method == 'POST':

        try: 

            nueva_cita = Citas(
                cliente = context['data'],
                inicio = request.POST['inicio'],
                final = request.POST['final'],
                asunto = request.POST['asunto'],
                descripción = request.POST['descrip']
            )

            nueva_cita.save()
            cita = Citas.objects.get(id = nueva_cita.id)
            asunto_nombre = str(nueva_cita.cliente.nombre) + ", " + str(nueva_cita.cliente.apellido) + ": " + str(nueva_cita.asunto)
            crear_evento(cita.inicio.isoformat(),
            cita.final.isoformat(), asunto_nombre, cita.descripción)

        except:
            pass
        try:
            context['data'].dni = request.FILES['dni']
            context['data'].save()
        except:
            pass
        try:
            context['data'].servicio = request.FILES['servicio']
            context['data'].save()
        except:
            pass
        try:
            context['data'].informe_crediticio = request.FILES['informe_crediticio']
            context['data'].save()
        except:
            pass
        try:
            context['data'].otros_datos = request.POST['otros_datos']
            context['data'].save()
        except:
            pass

        try:

            try:
                cuil = context['data'].cuil
                usuario = User.objects.get(username = cuil)
                usuario.username = request.POST['cuil']
                usuario.password = request.POST['cuil']
                usuario.save()

            except:
                pass

            context['data'].nombre = request.POST['nombre']
            context['data'].apellido = request.POST['apellido']
            context['data'].direccion = request.POST['direccion']
            context['data'].cuil = request.POST['cuil']
            context['data'].email = request.POST['email']
            context['data'].telefono = request.POST['telefono']
            context['data'].score = request.POST['score']
            context['data'].empleador = request.POST['empleador']
            context['data'].empresa = Empresa.objects.get(nombre = request.POST['empresa'])
            context['data'].save()

            
        except:
            pass 

    
    context['empresas'] = Empresa.objects.all()
     
    prestamos = Prestamos.objects.filter(cliente = context['data'])
    data_credite_complete = []

    for prestamo in prestamos:
        pagos = sum(Pagos.objects.filter(prestamo = prestamo).values_list("monto", flat=True))

        try:
            ultimo_pago = Pagos.objects.filter(prestamo = prestamo).order_by("-fecha")[0].fecha
        except:
            ultimo_pago = 0
        
        cuotas = CuotasPrestamo.objects.filter(prestamo = prestamo)
        monto_prestamo = sum(np.array(cuotas.values_list("monto", flat=True))) + sum(np.array(cuotas.values_list("monto_interes", flat=True))) - sum(np.array(cuotas.values_list("monto_bonificado", flat=True)))
        avance = pagos/monto_prestamo*100
        data_credite_complete.append((prestamo, pagos, ultimo_pago, avance))

    context['data_credite_complete'] = data_credite_complete
    context['citas'] = Citas.objects.filter(cliente = context['data'], inicio__gte = datetime.date.today()).order_by("-id")

    return render(request, "clientes/client_profile.html", context)

def newclientes(request):

    mensaje = 0

    empresas = Empresa.objects.all()

    if request.method == 'POST':

        if len(Clientes.objects.filter(cuil = request.POST['cuil'])) > 0:
            mensaje = "Ya existe el cliente en la base de datos"
        else:
            b = Clientes(
                nombre = request.POST['nombre'],
                apellido = request.POST['apellido'],
                direccion = request.POST['direccion'],
                cuil = request.POST['cuil'],
                telefono = request.POST['telefono'],
                score = request.POST['score'],
                email = request.POST['email'],
                empresa = Empresa.objects.get(nombre = request.POST['empresa']),
            )

            b.save()

            return redirect('BBDD clientes')

    return render(request, "clientes/cliente_new.html", {"mensaje":mensaje, "empresas":empresas})
