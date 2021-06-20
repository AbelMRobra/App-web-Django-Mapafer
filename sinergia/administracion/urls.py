from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^login$', views.login, name = 'Login'),
    url(r'^logout$', views.logout, name = 'Logout'),
    url(r'^$', views.welcome, name = 'Welcome'),
    url(r'^home$', login_required(views.home), name = 'Home'),

    # URL de clientes
    url(r'^bbdd$', login_required(views.clientes), name = 'BBDD clientes'),
    url(r'^newcliente$', login_required(views.newclientes), name = 'Nuevo cliente'),
    url(r'^client_profile/(?P<id_cliente>\d+)/$', login_required(views.profileclient), name = 'Perfil del cliente'),

    # URL de Externos

    url(r'^consulta_externo/(?P<code_key>\d+)/$', views.consulta_usuario_externo, name = 'Consulta externo'),

    # URL de Prestamos
    url(r'^principal$', login_required(views.cartera_activa), name = 'Principal Prestamos'),
    url(r'^newcredito$', login_required(views.newcredito), name = 'Nuevo credito'),
    url(r'^infoprestamo$', login_required(views.informacion_prestamos), name = 'Información Prestamos'),
    url(r'^cashflow$', login_required(views.cashflow), name = 'Cash Flow'),

    # URL de Info
    url(r'^infoaclaraciones$', login_required(views.aclaraciones), name = 'Aclaraciones'),
    

]