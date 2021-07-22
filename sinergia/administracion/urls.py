from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from . import views_pagos
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^login$', views.login, name = 'Login'),
    url(r'^logout$', views.logout, name = 'Logout'),
    url(r'^$', views.welcome, name = 'Welcome'),
    url(r'^home$', login_required(views.home), name = 'Home'),

    # URL de clientes
    url(r'^panelpagos$', login_required(views_pagos.pagos_panel), name = 'Panel de pagos'),
    url(r'^agregarpago/(?P<id_prestamo>\d+)/$', login_required(views_pagos.pagos_agregar), name = 'Agregar pagos'),

    # URL de clientes
    url(r'^bbdd$', login_required(views.clientes), name = 'BBDD clientes'),
    url(r'^newcliente$', login_required(views.newclientes), name = 'Nuevo cliente'),
    url(r'^client_profile/(?P<id_cliente>\d+)/$', login_required(views.profileclient), name = 'Perfil del cliente'),

    # URL de Externos

    url(r'^consulta_externo/(?P<code_key>\d+)/$', views.consulta_usuario_externo, name = 'Consulta externo'),

    # URL de Prestamos
    url(r'^principal$', login_required(views.cartera_activa), name = 'Principal Prestamos'),
    url(r'^newcredito$', login_required(views.newcredito), name = 'Nuevo credito'),
    url(r'^admincredito/(?P<id_credito>\d+)/$', login_required(views.administrar_credito), name = 'Administrar credito'),
    url(r'^infoprestamo$', login_required(views.informacion_prestamos), name = 'Información Prestamos'),
    url(r'^cashflow$', login_required(views.cashflow), name = 'Cash Flow'),

    # URL de Info
    url(r'^infoaclaraciones$', login_required(views.aclaraciones), name = 'Aclaraciones'),

    # URL de proveedores
    url(r'^newproveedores$', login_required(views.newproveedor), name = 'Nuevo proveedor'),
    

]