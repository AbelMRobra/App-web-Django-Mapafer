from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.urls.conf import include
from . import views
from .views_programa import views_proveedores, views_prestamos, views_pagos
from . import views_empresa
from . import views_clientes
from django.contrib.auth.decorators import login_required
from rest_framework import routers
from administracion.viewsets import viewsets_tasas, viewsets_empresa, viewsets_pagos, viewsets_prestamos


router = routers.DefaultRouter()
router.register(r'api_tasas', viewsets_tasas.TasasViewset)
router.register(r'api_empresa', viewsets_empresa.EmpresaViewset)
router.register(r'api_contacto', viewsets_empresa.ContactosEmpresaViewset)
router.register(r'api_pagos', viewsets_pagos.PagosViewset)
router.register(r'api_prestamos', viewsets_prestamos.PrestamosViewset)


urlpatterns = [

    path("api/", include(router.urls)),


    url(r'^login$', views.login, name = 'Login'),
    url(r'^logout$', views.logout, name = 'Logout'),
    url(r'^$', views.welcome, name = 'Welcome'),
    url(r'^home$', login_required(views.home), name = 'Home'),

    # URL de empresas
    url(r'^panelempresas$', login_required(views_empresa.panelempresas), name = 'Panel de empresas'),
    url(r'^panelempresas/(?P<id_empresa>\d+)/$', login_required(views_empresa.panel_pagos), name = 'Pagos por empresas'),
    url(r'^perfilempresa/(?P<id_empresa>\d+)/$', login_required(views_empresa.perfilempresa), name = 'Perfil empresa'),

    # URL de pagos
    url(r'^panelpagos$', login_required(views_pagos.pagos_panel), name = 'Panel de pagos'),
    url(r'^agregarpago/(?P<id_prestamo>\d+)/$', login_required(views_pagos.pagos_agregar), name = 'Agregar pagos'),
    url(r'^editarpago/(?P<id_pago>\d+)/$', login_required(views_pagos.pagos_editar), name = 'Editar pagos'),

    # URL de clientes
    url(r'^bbdd$', login_required(views_clientes.clientes), name = 'BBDD clientes'),
    url(r'^newcliente$', login_required(views_clientes.newclientes), name = 'Nuevo cliente'),
    url(r'^client_profile/(?P<id_cliente>\d+)/$', login_required(views_clientes.profileclient), name = 'Perfil del cliente'),

    # URL de Externos

    url(r'^consulta_externo/(?P<code_key>\d+)/$', views.consulta_usuario_externo, name = 'Consulta externo'),

    # URL de Prestamos
    url(r'^prestamo_principal$', login_required(views_prestamos.prestamos_panel), name = 'Principal Prestamos'),
    url(r'^prestamo_agregar$', login_required(views_prestamos.prestamos_agregar), name = 'Calculadora'),
    url(r'^prestamo_refinanciar$', login_required(views_prestamos.prestamos_refinanciar), name = 'Refinanciar'),
    url(r'^prestamo_cargado/(?P<id_credito_nuevo>\d+)/(?P<id_credito_anterior>\d+)/$', login_required(views_prestamos.prestamos_credito_cargado), name = 'Cargado'),
    url(r'^prestamo_info/(?P<id_credito>\d+)/$', login_required(views_prestamos.prestamos_detalle_completo), name = 'Administrar credito'),
    url(r'^infoprestamo$', login_required(views_prestamos.prestamos_informacion), name = 'Información Prestamos'),
    url(r'^cashflow$', login_required(views.cashflow), name = 'Cash Flow'),

    # URL de Info
    url(r'^infoaclaraciones$', login_required(views.aclaraciones), name = 'Aclaraciones'),

    # URL de proveedores
    url(r'^proveedoragregar/$', login_required(views_proveedores.proveedor_agregar), name = 'Nuevo proveedor'),
    url(r'^proveedoreditar/(?P<id_proveedor>\d+)/$', login_required(views_proveedores.proveedor_editar), name = 'Editar proveedor'),
    url(r'^pagosproveedor/(?P<id_proveedor>\d+)/$', login_required(views_proveedores.proveedor_pagos), name = 'Pago proveedor'),
    url(r'^proveedorpanel/$', login_required(views_proveedores.proveedor_panel), name = 'Panel proveedor'),
    

]