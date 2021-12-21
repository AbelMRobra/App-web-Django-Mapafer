from django.contrib import admin
from .models import Clientes, Proveedor, Prestamos, Pagos, Empresa, CuotasPrestamo, Citas, DeudaProveedor, \
    UserProfile
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class ClientesResource(resources.ModelResource):
    class Meta:
        model = Clientes

class ClientesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('nombre', 'apellido',  'cuil')
    search_fields = ('nombre', 'apellido',  'cuil')
    resources_class = ClientesResource

class EmpresaResource(resources.ModelResource):
    class Meta:
        model = Empresa

class EmpresaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']
    resources_class = EmpresaResource

class ProveedorResource(resources.ModelResource):
    class Meta:
        model = Proveedor

class ProveedorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('razon_social', 'fantasia')
    search_fields = ('razon_social', 'fantasia')
    resources_class = ProveedorResource

class PrestamosResource(resources.ModelResource):
    class Meta:
        model = Prestamos

class PrestamosAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('cliente', 'monto', 'regimen')
    search_fields = ('monto', 'regimen')
    resources_class = PrestamosResource

class PagosResource(resources.ModelResource):
    class Meta:
        model = Pagos

class PagosAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('fecha', 'monto')
    search_fields = ('fecha', 'monto')
    resources_class = PagosResource

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Clientes, ClientesAdmin)
admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(Prestamos, PrestamosAdmin)
admin.site.register(Pagos, PagosAdmin)
admin.site.register(CuotasPrestamo)
admin.site.register(Citas)
admin.site.register(UserProfile)
admin.site.register(DeudaProveedor)