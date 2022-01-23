import datetime
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from numpy import mod
from administracion.variables import *

# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=CASCADE, verbose_name="User", related_name='user')
    user_rol = models.CharField(choices=USER_ROL, default=USUARIO, max_length=10)
    imagen = models.ImageField(verbose_name="Imagen", blank=True, null=True)

    def __str__(self):
        return self.user.username

class Proveedor(models.Model):
    razon_social = models.CharField(max_length=200, verbose_name="Razón social")
    fantasia = models.CharField(max_length=200, verbose_name="Nombre de fantasia")

    class Meta:
        verbose_name="Proveedor"
        verbose_name_plural="Proveedores"

    def __str__(self):
        return self.razon_social

class TasaParaCreditos(models.Model):

    nombre = models.CharField(max_length=200, verbose_name="Nombre tasa")
    valor_tasa = models.FloatField(verbose_name="Valor de la tasa")

    class Meta:
        unique_together = (("nombre", "valor_tasa"))
        verbose_name="Tasa para credito"
        verbose_name_plural="Tasas para creditos"

    def __str__(self):
        return self.nombre

class Empresa(models.Model):

    nombre = models.CharField(max_length=200, verbose_name="Nombre", unique=True)
    password = models.CharField(max_length=200, verbose_name="password", blank=True, null=True)
    code_key = models.IntegerField(verbose_name="Code key", blank=True, null=True)

    telefono = models.CharField(max_length=200, verbose_name="Telefono", blank=True, null=True)
    contacto = models.CharField(max_length=200, verbose_name="Contacto", blank=True, null=True)
    rubro = models.CharField(max_length=200, verbose_name="Rubro", blank=True, null=True)
    direccion = models.CharField(max_length=200, verbose_name="Direccion", blank=True, null=True)
    email = models.CharField(max_length=200, verbose_name="Email", blank=True, null=True)

    class Meta:
        verbose_name="Empresa"
        verbose_name_plural="Empresas"

    def __str__(self):
        return self.nombre

class ContactosEmpresa(models.Model):

    empresa = models.ForeignKey(Empresa, verbose_name="Empresa", on_delete=CASCADE)
    contacto = models.CharField(max_length=30, verbose_name="Contacto")
    cargo = models.CharField(max_length=30, verbose_name="Cargo que ocupa", blank=True, null=True)
    numero = models.CharField(max_length=20, verbose_name="Telfono")
    email = models.CharField(max_length=30, verbose_name="Email")

    class Meta:
        unique_together = (("contacto", "numero"))
        verbose_name="Contacto"
        verbose_name_plural="Contactos"

    def __str__(self):
        return self.contacto

class Clientes(models.Model):

    usuario = models.ForeignKey(UserProfile, on_delete=models.PROTECT, verbose_name="Usuario del sistema", blank=True, null=True)
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    apellido = models.CharField(max_length=200, verbose_name="Apellido")
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name = "Empresa", blank=True, null=True)
    empleador = models.CharField(max_length=400, verbose_name="Empleador", blank=True, null=True)
    contacto = models.CharField(max_length=400, verbose_name="Contacto", blank=True, null=True)
    direccion = models.CharField(max_length=400, verbose_name="Dirección", blank=True, null=True)
    cuil = models.CharField(max_length=200, verbose_name="CUIL", blank=True, null=True, unique=True)
    telefono = models.CharField(max_length=200, verbose_name="Telefono", blank=True, null=True)
    email = models.CharField(max_length=200, verbose_name="Email", blank=True, null=True)
    score = models.IntegerField(verbose_name="Score", blank=True, null=True)
    otros_datos = models.TextField(verbose_name="Otros datos", blank=True, null=True)
    dni = models.FileField(verbose_name="Dni", blank=True, null=True)
    servicio = models.FileField(verbose_name="Servicio", blank=True, null=True)
    informe_crediticio = models.FileField(verbose_name="Informe crediticio", blank=True, null=True)
    imagen = models.ImageField(verbose_name="Imagen", blank=True, null=True)

    def estado_cliente(self):
        
        prestamos = Prestamos.objects.filter(cliente = self)
        today = datetime.date.today()

        estados = []
        
        if len(prestamos) > 0:
            
            for prestamo in prestamos:

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

    class Meta:
        verbose_name="Cliente"
        verbose_name_plural="Clientes"

    def __str__(self):
        return self.apellido

class Citas(models.Model):

    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, verbose_name = "Cliente")
    inicio = models.DateTimeField(verbose_name="Fecha de inicio")
    final = models.DateTimeField(verbose_name="Fecha final")
    asunto = models.CharField(max_length=100, verbose_name="Asunto")
    descripción = models.CharField(max_length=100, verbose_name="Descripción")

    class Meta:
        verbose_name="Cita"
        verbose_name_plural="Citas"

    def __str__(self):
        return self.asunto

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
    entregado = models.BooleanField(default=False, verbose_name="Se entrego el material/ dinero")


    def pagado_credito(self):

        pagado = sum(Pagos.objects.filter(prestamo = self).values_list("monto", flat=True))

        return pagado


    def saldo_credito(self):

        interes = sum(CuotasPrestamo.objects.filter(prestamo = self).values_list("monto_interes", flat=True))

        bonificacion = sum(CuotasPrestamo.objects.filter(prestamo = self).values_list("monto_bonificado", flat=True))

        pagos = sum(Pagos.objects.filter(prestamo = self).values_list("monto", flat=True))

        saldo = self.monto - pagos + interes + bonificacion

        return saldo

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
    fecha = models.DateField(verbose_name="Fecha de vencimiento")
    fecha_pago = models.DateField(verbose_name="Fecha de pago", blank=True, null=True)
    monto = models.FloatField(verbose_name="Monto")
    monto_interes = models.FloatField(verbose_name="Monto interes", blank=True, null=True, default=0)
    monto_bonificado = models.FloatField(verbose_name="Monto bonificado", blank=True, null=True, default=0)
    numero = models.IntegerField(verbose_name= "Numero", blank=True, null=True, default=1)
    estado = models.CharField(choices=Pagado.choices, max_length=20, verbose_name="Estado", blank=True, null=True)

    class Meta:
        verbose_name="Cuota"
        verbose_name_plural="Cuotas"

    def __str__(self):
        return self.estado

class Pagos(models.Model):

    comentarios = models.CharField(max_length=100, blank=True, null=True, verbose_name="Comentarios")
    prestamo = models.ForeignKey(Prestamos, on_delete=models.CASCADE, verbose_name = "Prestamo")
    fecha = models.DateField(verbose_name="Fecha del pago")
    monto = models.FloatField(verbose_name="Monto")

    class Meta:
        verbose_name="Pago"
        verbose_name_plural="Pagos"

class DeudaProveedor(models.Model):
    
    prestamo = models.ForeignKey(Prestamos, on_delete=models.SET_NULL, verbose_name = "Prestamo",blank=True, null=True)
    fecha = models.DateField(verbose_name="Fecha del pago")
    estado_pagado = models.BooleanField(default=False, verbose_name="Estado de la deuda")

    class Meta:
        verbose_name="Deuda con proveedores"
        verbose_name_plural="Deudas con proveedores"

    def __str__(self):
        return f'{self.prestamo.proveedor.razon_social}, {self.prestamo.valor_original}'

class PagosProveedores(models.Model):

    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name = "Cliente",blank=True, null=True)
    deuda = models.ForeignKey(DeudaProveedor, on_delete=models.SET_NULL, verbose_name = "Deuda",blank=True, null=True)
    fecha = models.DateField(verbose_name="Fecha del pago")
    monto = models.FloatField(verbose_name="Monto")

    class Meta:
        verbose_name="Pago a proveedor"
        verbose_name_plural="Pagos a proveedores"

    def __str__(self):
        return self.proveedor.fantasia