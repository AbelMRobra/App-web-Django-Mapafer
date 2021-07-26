from django.db import models

# Create your models here.

class Empresa(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    password = models.CharField(max_length=200, verbose_name="password", blank=True, null=True)
    code_key = models.IntegerField(verbose_name="Code key", blank=True, null=True)

    class Meta:
        verbose_name="Empresa"
        verbose_name_plural="Empresas"

    def __str__(self):
        return self.nombre

class Clientes(models.Model):

    class vivienda(models.TextChoices):
        PRESTADO = "PRESTADO"
        ALQUILADO = "ALQUILADO"
        TOMADO = "TOMADO"
        PROPIO_S_TITULO_S_BOLETO = "PROPIO SIN TITULO Y SIN BOLETO"
        PROPIO_BOLETO = "PROPIO CON BOLETO DE COMPRA-VENTA"
        PROPIO_S_TITULO_S_BOLETO_CONS = "PROPIO SIN TITULO Y SIN BOLETO, CON CONSTANCIA POLICIAL"
        OTRO = "OTRO"

    class siono(models.TextChoices):
        SI = "SI"
        NO = "NO"

    class situacionbath(models.TextChoices):
        ADENTRO = "ADENTRO"
        AFUERA = "AFUERA"

    class Estado(models.TextChoices):

        potencial = "Potencial"
        rechazado = "Rechazado"
        no_activo = "No activo"
        moroso_1 = "Situación 1"
        moroso_2 = "Situación 2"
        moroso_3 = "Situación 3"
        moroso_4 = "Situación 4"
        moroso_5 = "Situación 5"
        moroso_6 = "Situación 6"

    password = models.CharField(max_length=200, verbose_name="password", blank=True, null=True)
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    apellido = models.CharField(max_length=200, verbose_name="Apellido")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name = "Empresa", blank=True, null=True)
    empleador = models.CharField(max_length=400, verbose_name="Empleador", blank=True, null=True)
    contacto = models.CharField(max_length=400, verbose_name="Contacto", blank=True, null=True)
    direccion = models.CharField(max_length=400, verbose_name="Dirección", blank=True, null=True)
    cuil = models.CharField(max_length=200, verbose_name="CUIL", blank=True, null=True)
    telefono = models.CharField(max_length=200, verbose_name="Telefono", blank=True, null=True)
    email = models.CharField(max_length=200, verbose_name="Email", blank=True, null=True)
    score = models.IntegerField(verbose_name="Score", blank=True, null=True)
    estado = models.CharField(choices=Estado.choices, max_length=20, verbose_name="Estado", default="Potencial")
    otros_datos = models.TextField(verbose_name="Otros datos", blank=True, null=True)
    code_key = models.IntegerField(verbose_name="Code key", blank=True, null=True)
    dni = models.FileField(verbose_name="Dni", blank=True, null=True)
    servicio = models.FileField(verbose_name="Servicio", blank=True, null=True)
    informe_crediticio = models.FileField(verbose_name="Informe crediticio", blank=True, null=True)
    imagen = models.ImageField(verbose_name="Imagen", blank=True, null=True)

    # Parte social
    habitantes_hogar = models.IntegerField(verbose_name="Habitantes del hogar", blank=True, null=True)
    trabajadores_hogar = models.IntegerField(verbose_name="Trabajadores del hogar", blank=True, null=True)
    ingreso_hogar = models.IntegerField(verbose_name="Ingreso hogar", blank=True, null=True)
    cuartos = models.IntegerField(verbose_name="Ambientes", blank=True, null=True)
    bathrooms = models.IntegerField(verbose_name="Dormitorios", blank=True, null=True)

    partiente_discapacidad = models.CharField(choices=siono.choices, max_length=20, verbose_name="Pariente con discapacidad", blank=True, null=True)
    gas = models.CharField(choices=siono.choices, max_length=20, verbose_name="Gas", blank=True, null=True)
    cloaca = models.CharField(choices=siono.choices, max_length=20, verbose_name="Cloaca", blank=True, null=True)
    agua_corriente = models.CharField(choices=siono.choices, max_length=20, verbose_name="Agua corriente", blank=True, null=True)
    deuda = models.CharField(choices=siono.choices, max_length=20, verbose_name="Deuda entidad bancaria", blank=True, null=True)

    titulo_vivienda = models.CharField(choices=vivienda.choices, max_length=100, verbose_name="Vivienda", blank=True, null=True)
    bath_sit = models.CharField(choices=situacionbath.choices, max_length=100, verbose_name="Baño situación", blank=True, null=True)



    class Meta:
        verbose_name="Cliente"
        verbose_name_plural="Clientes"

    def __str__(self):
        return self.apellido

class Proveedor(models.Model):
    razon_social = models.CharField(max_length=200, verbose_name="Razón social")
    fantasia = models.CharField(max_length=200, verbose_name="Nombre de fantasia")

    class Meta:
        verbose_name="Proveedor"
        verbose_name_plural="Proveedores"

    def __str__(self):
        return self.razon_social

class Prestamos(models.Model):

    class Regimen(models.TextChoices):
        QUINCENAL = "QUINCENAL"
        MENSUAL = "MENSUAL"

    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, verbose_name = "Cliente")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name = "Proveedor")
    fecha = models.DateTimeField(verbose_name="Fecha del prestamo")
    primera_cuota = models.DateTimeField(verbose_name="Primera cuota")
    valor_original = models.FloatField(verbose_name="Valor original", blank=True, null=True)
    presupuesto_cliente = models.FloatField(verbose_name="Presupuesto cliente", blank=True, null=True)
    monto = models.FloatField(verbose_name="Monto")
    cuotas = models.IntegerField(verbose_name="Cuotas")
    regimen = models.CharField(choices=Regimen.choices, max_length=20, verbose_name="Regimen")
    adjunto = models.FileField(verbose_name="Adjunto", blank=True, null=True)

    class Meta:
        verbose_name="Prestamo"
        verbose_name_plural="Prestamos"

    def __str__(self):
        return self.cliente.nombre

class CuotasPrestamo(models.Model):

    class Pagado(models.TextChoices):
        NO = "NO"
        SI = "SI"
        PARCIAL = "PARCIAL"

    prestamo = models.ForeignKey(Prestamos, on_delete=models.CASCADE, verbose_name = "Prestamo asociado")
    fecha = models.DateField(verbose_name="Fecha del pago")
    monto = models.FloatField(verbose_name="Monto")
    estado = models.CharField(choices=Pagado.choices, max_length=20, verbose_name="Estado", blank=True, null=True)

    class Meta:
        verbose_name="Cuota"
        verbose_name_plural="Cuotas"

    def __str__(self):
        return self.fecha

class Pagos(models.Model):
    prestamo = models.ForeignKey(Prestamos, on_delete=models.CASCADE, verbose_name = "Prestamo")
    fecha = models.DateField(verbose_name="Fecha del pago")
    monto = models.FloatField(verbose_name="Monto")

    class Meta:
        verbose_name="Pago"
        verbose_name_plural="Pagos"