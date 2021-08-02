from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from .models import Clientes, Prestamos, Pagos, Proveedor, Empresa, CuotasPrestamo
import numpy as np
import datetime
from .functions import estado_cliente


# Create your views here.

def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        if len(Clientes.objects.filter(cuil = request.POST['username'], password = request.POST['password'])):

            cliente = Clientes.objects.get(cuil = request.POST['username'], password = request.POST['password'])

            code_key_new = str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))

            while len(Clientes.objects.filter(code_key = int(code_key_new))) > 0:

                code_key_new = str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))

            cliente.code_key = int(code_key_new)
            cliente.save()

            return redirect('Consulta externo', code_key = cliente.code_key)

        if len(Empresa.objects.filter(nombre = request.POST['username'], password = request.POST['password'])):

            empresa = Empresa.objects.get(nombre = request.POST['username'], password = request.POST['password'])

            code_key_new = str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))

            while len(Empresa.objects.filter(code_key = int(code_key_new))) > 0:

                code_key_new = str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))

            empresa.code_key = int(code_key_new)
            empresa.save()

            return redirect('Consulta externo', code_key = empresa.code_key)

        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

        else:

            mensaje = "Usuario/contraseña incorrectos"

            return render(request, "login.html", {'form': form, 'mensaje':mensaje}) 

    # Si llegamos al final renderizamos el formulario

    return render(request, "login.html", {'form': form})

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')

def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:

        return render(request, "welcome.html")
    # En otro caso redireccionamos al login
    return redirect('/login')

def home(request):

    today = datetime.date.today()

    ### Conjunto de fechas para el flujo de ingresos

    if today.day > 15:
        if today.month == 12:
            fecha_cash_inicial = datetime.date(today.year, 1, 1)
        else:
            fecha_cash_inicial = datetime.date(today.year, today.month + 1, 1)      
    else:
        fecha_cash_inicial = datetime.date(today.year, today.month, 1)

    fechas_cash = []

    fecha_cash_aux = fecha_cash_inicial

    for f in range(24):
        fechas_cash.append(fecha_cash_aux)
        if fecha_cash_aux.month == 12:
            fecha_cash_aux = datetime.date(fecha_cash_aux.year + 1, 1, 1)
        else:
            fecha_cash_aux = datetime.date(fecha_cash_aux.year, fecha_cash_aux.month + 1, 1)

    ### Aqui termina la programación para el conjunto de fechas para el flujo de ingreso

    # Bucle para mora y flujo de ingresos

    matriz_ones = []
    matriz_ingresos = []
    mora_total = 0
    data_aux = Prestamos.objects.all()

    for d in data_aux:
        datos_cuenta = []   
        pagos_list = Pagos.objects.filter(prestamo = d).values_list("monto", flat = True)
        pagos = sum(pagos_list)
        saldo = d.monto - pagos
        fecha_primer_pago = datetime.date(d.primera_cuota.year, d.primera_cuota.month, d.primera_cuota.day)
        if d.regimen == "QUINCENAL":
            cuotas_pasadas = 0
            fecha_aux = fecha_primer_pago
            while fecha_aux < today:
                cuotas_pasadas +=1
                if cuotas_pasadas == d.cuotas:
                    break
                else:
                    fecha_aux = fecha_aux + datetime.timedelta(days=15)
            mora = cuotas_pasadas*(d.monto/d.cuotas) - pagos
            mora_total += mora

            for f in range(24):
                situacion_1 = 1
                if fecha_cash_inicial.day > 15:
                    situacion_1 = 1
                else:
                    situacion_1 = 0

                if situacion_1 == 1:
                    cuotas_pendientes = d.cuotas - cuotas_pasadas
                    if cuotas_pendientes == 1:
                        pago_mes = (d.monto/d.cuotas)
                        if saldo > pago_mes:
                            datos_cuenta.append(pago_mes)
                            cuotas_pasadas += 1
                            saldo = saldo - pago_mes
                        elif saldo <= 0:
                            datos_cuenta.append(0)
                            cuotas_pasadas += 1
                        else:
                            datos_cuenta.append(saldo)
                            cuotas_pasadas += 1
                            saldo = 0

                    else:
                        datos_cuenta.append(0)

                    situacion_1 = 0
                else:
                    cuotas_pendientes = d.cuotas - cuotas_pasadas
                    if cuotas_pendientes >= 2:
                        pago_mes = (d.monto/d.cuotas*2)
                        if saldo > pago_mes:
                            datos_cuenta.append(pago_mes)
                            cuotas_pasadas += 2
                            saldo = saldo - pago_mes
                        elif saldo <= 0:
                            datos_cuenta.append(0)
                            cuotas_pasadas += 2
                        else:
                            datos_cuenta.append(saldo)
                            cuotas_pasadas += 2
                            saldo = 0

                    elif cuotas_pendientes == 1:
                        pago_mes = (d.monto/d.cuotas)
                        if saldo > pago_mes:
                            datos_cuenta.append(pago_mes)
                            cuotas_pasadas += 1
                            saldo = saldo - pago_mes
                        elif saldo <= 0:
                            datos_cuenta.append(0)
                            cuotas_pasadas += 1
                        else:
                            datos_cuenta.append(saldo)
                            cuotas_pasadas += 1
                            saldo = 0

                    else:
                        datos_cuenta.append(0)

        if d.regimen == "MENSUAL":
            cuotas_pasadas = 0
            fecha_aux = fecha_primer_pago
            while fecha_aux < today:
                cuotas_pasadas +=1
                if cuotas_pasadas == d.cuotas:
                    break
                else:
                    if fecha_aux.month != 12:
                        fecha_aux = datetime.date(fecha_aux.year, fecha_aux.month +1, fecha_aux.day)
                    else:
                        fecha_aux = datetime.date(fecha_aux.year + 1, 1, fecha_aux.day)
            mora = cuotas_pasadas*(d.monto/d.cuotas) - pagos
            mora_total += mora
            for f in range(24):
                cuotas_pendientes = d.cuotas - cuotas_pasadas
                if cuotas_pendientes >= 1:
                    pago_mes = (d.monto/d.cuotas)
                    if saldo > pago_mes:
                        datos_cuenta.append(pago_mes)
                        cuotas_pasadas += 1
                        saldo = saldo - pago_mes
                    elif saldo <= 0:
                        datos_cuenta.append(0)
                        cuotas_pasadas += 1
                    else:
                        datos_cuenta.append(saldo)
                        cuotas_pasadas += 1
                        saldo = 0
                else:
                    datos_cuenta.append(0)
        matriz_ingresos.append(datos_cuenta)
        matriz_ones.append(1)
    matriz_ingresos = np.array(matriz_ingresos)
    matriz_resultante = np.matmul(matriz_ones, matriz_ingresos)

    # Aqui termina la programación para ese calculo

    # Calculo del monto de interes y las TAE

    monto_interes = sum(Prestamos.objects.all().values_list('monto', flat = True)) - sum(Prestamos.objects.all().values_list('valor_original', flat = True))

    prestamos_year_courrent = Prestamos.objects.filter(fecha__gte = datetime.date(today.year, 1, 1))

    tae_year_courrent = []

    for d in prestamos_year_courrent:
        interes = (d.monto/d.valor_original - 1)*100
        tae = (interes/d.cuotas)*12
        tae_year_courrent.append(tae)

    prom_tae_year_courrent = np.mean(tae_year_courrent)

    prestamos_year_last = Prestamos.objects.filter(fecha__range = (datetime.date(today.year -1, 1, 1), datetime.date(today.year, 1, 1)))

    tae_year_last = []

    for d in prestamos_year_last:
        interes = (d.monto/d.valor_original - 1)*100
        tae = (interes/d.cuotas)*12
        tae_year_last.append(tae)

    prom_tae_year_last = np.mean(tae_year_last)

    # Otros datos

    user_active = len(Clientes.objects.filter(estado = "Activo"))
    prestamos = len(Prestamos.objects.all())
    total_prestamos = sum(Prestamos.objects.all().values_list('monto', flat = True))
    total_pago = round((sum(Pagos.objects.all().values_list('monto', flat = True))/total_prestamos)*100, 0)
    total_saldo = round(((total_prestamos - sum(Pagos.objects.all().values_list('monto', flat = True)) - mora_total)/total_prestamos)*100, 0)
    monto_mora = mora_total
    monto_saldo = (total_prestamos - sum(Pagos.objects.all().values_list('monto', flat = True)) - mora_total)
    mora_total = round((mora_total/total_prestamos)*100, 0)

    # Información del grafico principal

    fechas_grafico = []

    fecha_inicial = datetime.date(today.year, today. month, 1)

    fecha_auxiliar = fecha_inicial
    for f in range(12):
        fechas_grafico.append(fecha_auxiliar)
        if fecha_auxiliar.month != 1:
            fecha_auxiliar = datetime.date(fecha_auxiliar.year, fecha_auxiliar.month -1 , fecha_auxiliar.day)
        else:
            fecha_auxiliar = datetime.date(fecha_auxiliar.year - 1, 12 , fecha_auxiliar.day)

    datos_grafico = []
    fecha_auxiliar = 0
    cont = 0
    for f in fechas_grafico:
        if cont == 0:
            fecha_auxiliar = f
            cont = 1
        else:
            monto = sum(Prestamos.objects.filter(fecha__range = (f, fecha_auxiliar)).values_list("monto", flat = True))
            datos_grafico.append((f, monto))
            fecha_auxiliar = f

    datos_grafico = sorted(datos_grafico, key=lambda x: x[0])
    monto_total = sum(Prestamos.objects.all().values_list("monto", flat=True))
    pago_total = sum(Pagos.objects.all().values_list("monto", flat=True))

    return render(request, "home.html", {"prom_tae_year_last":prom_tae_year_last, "prom_tae_year_courrent":prom_tae_year_courrent, "monto_interes":monto_interes, "matriz_resultante":matriz_resultante, "fechas_cash":fechas_cash,"monto_saldo":monto_saldo, "monto_mora":monto_mora, "pago_total":pago_total, "monto_total":monto_total, "datos_grafico":datos_grafico, "mora_total":mora_total, "user_active":user_active, "prestamos":prestamos, "total_saldo":total_saldo, "total_pago":total_pago})

def consulta_usuario_externo(request, code_key):

    try:

        try:
            tipo = "PERSONA"

            data = Clientes.objects.get(code_key = code_key)

            code_key_new = str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))

            while len(Clientes.objects.filter(code_key = int(code_key_new))) > 0:

                code_key_new = str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))+str(round(np.random.random()*9))

            data.code_key = int(code_key_new)
            data.save()

            creditos = Prestamos.objects.filter(cliente = data)
            data_pagos = Pagos.objects.filter(prestamo__cliente = data).order_by("-fecha")
            
            if len(creditos) > 0:

                data_credito = []

                for c in creditos:
                    monto_pagado = sum(Pagos.objects.filter(prestamo = c).values_list("monto", flat = True))
                    avance = (monto_pagado/c.monto)*100
                    try:
                        ultimo_pago = Pagos.objects.filter(prestamo = c).order_by("-fecha")[0].fecha
                    except:
                        ultimo_pago = 0
                    proxima_cuota = 'Aguanta'
                    monto_proxima = 0
                    mora = 0
                    fecha_primer_pago = datetime.date(c.primera_cuota.year, c.primera_cuota.month, c.primera_cuota.day)
                    today = datetime.date.today()
                    if c.regimen == "QUINCENAL":
                        cuotas_pasadas = 0
                        fecha_aux = fecha_primer_pago
                        while fecha_aux < today:
                            cuotas_pasadas +=1
                            if cuotas_pasadas == c.cuotas:
                                break
                            else:
                                fecha_aux = fecha_aux + datetime.timedelta(days=15)
                        mora = cuotas_pasadas*(c.monto/c.cuotas) - monto_pagado
                        if cuotas_pasadas < c.cuotas:
                            proxima_cuota = fecha_aux
                            monto_proxima = c.monto/c.cuotas
                        else:
                            proxima_cuota = 0
                            monto_proxima = 0
                        
                
                    if c.regimen == "MENSUAL":
                        cuotas_pasadas = 0
                        fecha_aux = fecha_primer_pago
                        while fecha_aux < today:
                            cuotas_pasadas +=1
                            if cuotas_pasadas == c.cuotas:
                                break
                            else:
                                if fecha_aux.month != 12:
                                    fecha_aux = datetime.date(fecha_aux.year, fecha_aux.month +1, fecha_aux.day)
                                else:
                                    fecha_aux = datetime.date(fecha_aux.year + 1, 1, fecha_aux.day)
                        mora = cuotas_pasadas*(c.monto/c.cuotas) - monto_pagado
                        if cuotas_pasadas < c.cuotas:
                            proxima_cuota = fecha_aux
                            monto_proxima = c.monto/c.cuotas
                        else:
                            proxima_cuota = 0
                            monto_proxima = 0

                    data_credito.append((c, monto_pagado, avance, ultimo_pago, proxima_cuota, monto_proxima, mora, (mora/(c.monto/c.cuotas))))

            else:

                data_credito = 0

        except:
            tipo = "EMPRESA"
            data = Empresa.objects.get(code_key = code_key)
            data_credito = []
            data_pagos = []

            prestamos_empresa = Prestamos.objects.filter(cliente__empresa = data).order_by("cliente__nombre")
            for c in prestamos_empresa:
                monto_pagado = sum(Pagos.objects.filter(prestamo = c).values_list("monto", flat = True))
                avance = (monto_pagado/c.monto)*100
                try:
                    ultimo_pago = Pagos.objects.filter(prestamo = c).order_by("-fecha")[0].fecha
                except:
                    ultimo_pago = 0
                proxima_cuota = 'Aguanta'
                monto_proxima = 0
                mora = 0
                fecha_primer_pago = datetime.date(c.primera_cuota.year, c.primera_cuota.month, c.primera_cuota.day)
                today = datetime.date.today()
                if c.regimen == "QUINCENAL":
                    cuotas_pasadas = 0
                    fecha_aux = fecha_primer_pago
                    while fecha_aux < today:
                        cuotas_pasadas +=1
                        if cuotas_pasadas == c.cuotas:
                            break
                        else:
                            fecha_aux = fecha_aux + datetime.timedelta(days=15)
                    mora = cuotas_pasadas*(c.monto/c.cuotas) - monto_pagado
                    if cuotas_pasadas < c.cuotas:
                        proxima_cuota = fecha_aux
                        monto_proxima = c.monto/c.cuotas
                    else:
                        proxima_cuota = 0
                        monto_proxima = 0
                    
            
                if c.regimen == "MENSUAL":
                    cuotas_pasadas = 0
                    fecha_aux = fecha_primer_pago
                    while fecha_aux < today:
                        cuotas_pasadas +=1
                        if cuotas_pasadas == c.cuotas:
                            break
                        else:
                            if fecha_aux.month != 12:
                                fecha_aux = datetime.date(fecha_aux.year, fecha_aux.month +1, fecha_aux.day)
                            else:
                                fecha_aux = datetime.date(fecha_aux.year + 1, 1, fecha_aux.day)
                    mora = cuotas_pasadas*(c.monto/c.cuotas) - monto_pagado
                    if cuotas_pasadas < c.cuotas:
                        proxima_cuota = fecha_aux
                        monto_proxima = c.monto/c.cuotas
                    else:
                        proxima_cuota = 0
                        monto_proxima = 0

                data_credito.append((c, monto_pagado, avance, ultimo_pago, proxima_cuota, monto_proxima, mora, (mora/(c.monto/c.cuotas))))


    except:

        return redirect('/')

    


    return render(request, "externo/consulta_externo.html", {'tipo':tipo, 'data': data, 'data_credito':data_credito, 'data_pagos':data_pagos})

def clientes(request):

    if request.method == 'POST':

        try:
            cliente = Clientes.objects.get(id = request.POST['borrar'])
            cliente.delete()
        except:
            pass

    data = Clientes.objects.all().order_by("nombre")

    for d in data:

        cliente_Estado = estado_cliente(d)
        d.estado = cliente_Estado
        d.save()

    return render(request, "clientes/basededatosclientes.html", {'data':data})

def profileclient(request, id_cliente):

    data = Clientes.objects.get(id = id_cliente)

    if request.method == 'POST':

        try:
            data.dni = request.FILES['dni']
            data.save()
        except:
            pass

        try:
            data.servicio = request.FILES['servicio']
            data.save()
        except:
            pass

        try:
            data.informe_crediticio = request.FILES['informe_crediticio']
            data.save()
        except:
            pass

        try:
            data.otros_datos = request.POST['otros_datos']
            data.save()
        except:
            pass

        try:
            data.nombre = request.POST['nombre']
            data.apellido = request.POST['apellido']
            data.direccion = request.POST['direccion']
            data.cuil = request.POST['cuil']
            data.email = request.POST['email']
            data.telefono = request.POST['telefono']
            data.score = request.POST['score']
            data.empleador = request.POST['empleador']
            data.empresa = Empresa.objects.get(nombre = request.POST['empresa'])
            data.save()
        except:
            pass 

    

    empresas = Empresa.objects.all()
     
    data_credito = Prestamos.objects.filter(cliente = data)

    data_credite_complete = []

    for d in data_credito:

        pagos = sum(Pagos.objects.filter(prestamo = d).values_list("monto", flat=True))
        try:
            ultimo_pago = Pagos.objects.filter(prestamo = d).order_by("-fecha")[0].fecha
        except:
            ultimo_pago = 0
        avance = pagos/d.monto*100

        data_credite_complete.append((d, pagos, ultimo_pago, avance))

    return render(request, "clientes/client_profile.html", {'empresas':empresas, 'data':data, "data_credite_complete":data_credite_complete})

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

def newcredito(request):

    clientes = Clientes.objects.all()
    proveedores = Proveedor.objects.all()

    if request.method == 'POST':
        new_credito = Prestamos(
            cliente = Clientes.objects.get(id = request.POST['cliente']),
            proveedor = Proveedor.objects.get(id = request.POST['proveedor']),
            fecha = request.POST['fecha'],
            primera_cuota = request.POST['priimeracuota'],
            valor_original = request.POST['precio1'],
            presupuesto_cliente = request.POST['precio3'],
            monto = request.POST['precio2'],
            cuotas = request.POST['cuotas'],
            regimen = request.POST['regimen'],
        )
        new_credito.save()
        try:
            new_credito.adjunto = request.FILES['adjunto']
            new_credito.save()
        except:
            pass

        return redirect('Principal Prestamos')

    return render(request, 'prestamos/nuevo_credito.html', {'clientes':clientes, 'proveedores':proveedores})



def administrar_credito(request, id_credito):

    credito = Prestamos.objects.get(id = id_credito)

    if request.method == 'POST':
        id_proveedor = request.POST['proveedor'].split("-")[0]
        proveedor = Proveedor.objects.get(id = int(id_proveedor))
        credito.proveedor = proveedor
        credito.valor_original = request.POST['valor_original']
        credito.monto = request.POST['monto']
        credito.cuotas = request.POST['cuotas']
        credito.presupuesto_cliente = request.POST['presupuesto_cliente']
        credito.fecha = request.POST['fecha']
        credito.save()

        if request.POST['primera_cuota'] != str(credito.primera_cuota):
            cuotas_prestamo = CuotasPrestamo.objects.filter(prestamo = credito)
            for c in cuotas_prestamo:
                c.delete()
            credito.primera_cuota = request.POST['primera_cuota']
            credito.save()

        return redirect('Administrar credito', id_credito = credito.id)


    cuotas = CuotasPrestamo.objects.filter(prestamo = credito)

    pagos = Pagos.objects.filter(prestamo = credito)

    total_pagado = sum(Pagos.objects.filter(prestamo = credito).values_list("monto", flat=True))

    proveedores = Proveedor.objects.all()

    context = {}
    context['credito'] = credito
    context['cuotas'] = cuotas
    context['pagos'] = pagos
    context['total_pagado'] = total_pagado
    context['proveedores'] = proveedores

    return render(request, 'prestamos/administrar_credito.html', context)

def informacion_prestamos(request):

    data = []

    data_aux = Prestamos.objects.all()

    for d in data_aux:
        interes = (d.monto/d.valor_original - 1)*100
        pagos = sum(Pagos.objects.filter(prestamo = d).values_list("monto", flat = True))
        avance = pagos/d.monto*100
        cuota = d.monto/d.cuotas
        tae = (interes/d.cuotas)*12
        aux = 1/360
        tna = (((1+tae)**aux)-1)*360
        data.append((d, interes, avance, cuota, tae, tna))

    return render(request, "prestamos/informacion.html", {'data':data})

def cartera_activa(request):

    if request.method == 'POST':
        consulta_borrar = Prestamos.objects.get(id = int(request.POST['borrar']))
        consulta_borrar.delete()

    data = []

    data_aux = Prestamos.objects.all()

    for d in data_aux:
        today = datetime.date.today()
        pagos_list = Pagos.objects.filter(prestamo = d).values_list("monto", flat = True)
        cant = len(pagos_list)
        pagos = sum(pagos_list)
        saldo = d.monto - pagos    
        fecha_prestamo = datetime.date(d.fecha.year, d.fecha.month, d.fecha.day)
        fecha_primer_pago = datetime.date(d.primera_cuota.year, d.primera_cuota.month, d.primera_cuota.day)
        if d.regimen == "QUINCENAL":
            cuotas_pasadas = 0
            fecha_aux = fecha_primer_pago
            while fecha_aux < today:
                cuotas_pasadas +=1
                if cuotas_pasadas == d.cuotas:
                    break
                else:
                    fecha_aux = fecha_aux + datetime.timedelta(days=15)
            mora = cuotas_pasadas*(d.monto/d.cuotas) - pagos

            prox_vencimiento = fecha_aux 
            data.append((d, pagos, saldo, prox_vencimiento, mora))
        if d.regimen == "MENSUAL":
            cuotas_pasadas = 0
            fecha_aux = fecha_primer_pago
            while fecha_aux < today:
                cuotas_pasadas +=1
                if cuotas_pasadas == d.cuotas:
                    break
                else:
                    if fecha_aux.month != 12:
                        fecha_aux = datetime.date(fecha_aux.year, fecha_aux.month +1, fecha_aux.day)
                    else:
                        fecha_aux = datetime.date(fecha_aux.year + 1, 1, fecha_aux.day)
            mora = cuotas_pasadas*(d.monto/d.cuotas) - pagos

            prox_vencimiento = fecha_aux 
            data.append((d, pagos, saldo, prox_vencimiento, mora))
    return render(request, "prestamos/panelprincipal.html", {'data':data})

def cashflow(request):

    today = datetime.date.today()

    # Creamos el conjunto de fechas

    if today.day > 15:
        if today.month == 12:
            fecha_cash_inicial = datetime.date(today.year, 1, 1)
        else:
            fecha_cash_inicial = datetime.date(today.year, today.month + 1, 1)      
    else:
        fecha_cash_inicial = datetime.date(today.year, today.month, 1)

    fechas_cash = []

    fecha_cash_aux = fecha_cash_inicial

    for f in range(24):
        fechas_cash.append(fecha_cash_aux)
        if fecha_cash_aux.month == 12:
            fecha_cash_aux = datetime.date(fecha_cash_aux.year + 1, 1, 1)
        else:
            fecha_cash_aux = datetime.date(fecha_cash_aux.year, fecha_cash_aux.month + 1, 1)

    data = []

    matriz_ones = []
    matriz_ingresos = []

    data_aux = Prestamos.objects.all().exclude(cliente__estado = "Moroso")

    for d in data_aux:
        datos_cuenta = []       
        pagos_list = Pagos.objects.filter(prestamo = d).values_list("monto", flat = True)
        pagos = sum(pagos_list)
        saldo = d.monto - pagos    
        fecha_primer_pago = datetime.date(d.primera_cuota.year, d.primera_cuota.month, d.primera_cuota.day)
        if d.regimen == "QUINCENAL":
            cuotas_pasadas = 0
            fecha_aux = fecha_primer_pago
            while fecha_aux < today:
                cuotas_pasadas +=1
                if cuotas_pasadas == d.cuotas:
                    break
                else:
                    fecha_aux = fecha_aux + datetime.timedelta(days=15)
            mora = cuotas_pasadas*(d.monto/d.cuotas) - pagos
            
            for f in range(24):
                situacion_1 = 1
                if fecha_cash_inicial.day > 15:
                    situacion_1 = 1
                else:
                    situacion_1 = 0

                if situacion_1 == 1:
                    cuotas_pendientes = d.cuotas - cuotas_pasadas
                    if cuotas_pendientes == 1:
                        pago_mes = (d.monto/d.cuotas)
                        if saldo > pago_mes:
                            datos_cuenta.append(pago_mes)
                            cuotas_pasadas += 1
                            saldo = saldo - pago_mes
                        elif saldo <= 0:
                            datos_cuenta.append(0)
                            cuotas_pasadas += 1
                        else:
                            datos_cuenta.append(saldo)
                            cuotas_pasadas += 1
                            saldo = 0

                    else:
                        datos_cuenta.append(0)

                    situacion_1 = 0
                else:
                    cuotas_pendientes = d.cuotas - cuotas_pasadas
                    if cuotas_pendientes >= 2:
                        pago_mes = (d.monto/d.cuotas*2)
                        if saldo > pago_mes:
                            datos_cuenta.append(pago_mes)
                            cuotas_pasadas += 2
                            saldo = saldo - pago_mes
                        elif saldo <= 0:
                            datos_cuenta.append(0)
                            cuotas_pasadas += 2
                        else:
                            datos_cuenta.append(saldo)
                            cuotas_pasadas += 2
                            saldo = 0

                    elif cuotas_pendientes == 1:
                        pago_mes = (d.monto/d.cuotas)
                        if saldo > pago_mes:
                            datos_cuenta.append(pago_mes)
                            cuotas_pasadas += 1
                            saldo = saldo - pago_mes
                        elif saldo <= 0:
                            datos_cuenta.append(0)
                            cuotas_pasadas += 1
                        else:
                            datos_cuenta.append(saldo)
                            cuotas_pasadas += 1
                            saldo = 0

                    else:
                        datos_cuenta.append(0)
        
        if d.regimen == "MENSUAL":
            cuotas_pasadas = 0
            fecha_aux = fecha_primer_pago
            while fecha_aux < today:
                cuotas_pasadas +=1
                if cuotas_pasadas == d.cuotas:
                    break
                else:
                    if fecha_aux.month != 12:
                        fecha_aux = datetime.date(fecha_aux.year, fecha_aux.month +1, fecha_aux.day)
                    else:
                        fecha_aux = datetime.date(fecha_aux.year + 1, 1, fecha_aux.day)
            mora = cuotas_pasadas*(d.monto/d.cuotas) - pagos

            for f in range(24):
                cuotas_pendientes = d.cuotas - cuotas_pasadas
                if cuotas_pendientes >= 1:
                    pago_mes = (d.monto/d.cuotas)
                    if saldo > pago_mes:
                        datos_cuenta.append(pago_mes)
                        cuotas_pasadas += 1
                        saldo = saldo - pago_mes
                    elif saldo <= 0:
                        datos_cuenta.append(0)
                        cuotas_pasadas += 1
                    else:
                        datos_cuenta.append(saldo)
                        cuotas_pasadas += 1
                        saldo = 0
                else:
                    datos_cuenta.append(0)

        data.append((d, datos_cuenta))
        matriz_ingresos.append(datos_cuenta)
        matriz_ones.append(1)
    matriz_ingresos = np.array(matriz_ingresos)
    matriz_resultante = np.matmul(matriz_ones, matriz_ingresos)

    return render(request, "prestamos/cashflow.html", {"matriz_resultante":matriz_resultante, "fechas_cash":fechas_cash, "data_aux":data_aux, "data":data})


### ----------> Funciones para la sección INFO

def aclaraciones(request):
    return render(request, "info/aclaraciones.html")