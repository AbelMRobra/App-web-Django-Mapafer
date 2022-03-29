from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

from administracion.models import Prestamos, Proveedor, Clientes, TasaParaCreditos
from administracion.serializers import serializers_prestamos
from ..funciones.f_prestamos import *

class PrestamosViewset(viewsets.ModelViewSet):

    queryset = Prestamos.objects.all()
    serializer_class = serializers_prestamos.PrestamosSerializers
    permission_classes = (IsAuthenticated,)

    @action(methods=['GET'], detail=True)
    def datos_prestamo_actual(self, request, pk):
        
        try:
            prestamo = Prestamos.objects.get(id = pk)
            valor_cuota = prestamo.monto/prestamo.cuotas
            response = {"mensaje": "Success",
            "cliente": f"{prestamo.cliente.nombre}, {prestamo.cliente.apellido}",
            "cuota": round(valor_cuota, 2),
            "pagado": round(prestamo.pagado_credito(), 2),
            "saldo": round(prestamo.saldo_credito(), 2),}
            return Response(response, status=status.HTTP_202_ACCEPTED)

        except:

            response = {"mensaje": "No encontrado"}

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def consulta_datos_crear_prestamo(self, request):

        try:
            
            tasa = float(request.data['tasa'])
            monto_inicial = float(request.data['monto_incial'])
            periodo_gracia = int(request.data['peridos_gracia'])
            regimen = request.data['regimen']
            cantidad_cuotas = int(request.data['cantidad_cuotas'])

            datos_calculadora = prestamos_calculadora(tasa, monto_inicial, periodo_gracia, regimen, cantidad_cuotas)

            response = {}
            response["monto"] = round(datos_calculadora[0], 2)
            response["monto_cuota"] = datos_calculadora[1]
            response["cuota"] = datos_calculadora[2]
            response["simulacion"] = []

            if request.data['primera_cuota'] != "":
                primera_cuota = str(request.data['primera_cuota'])
                response["simulacion"] = simular_cuotas_prestamo(regimen, cantidad_cuotas, primera_cuota)

            return Response(response, status=status.HTTP_200_OK)

        except:

            response = {"mensaje": "No encontrado"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def consulta_datos_refinanciar_prestamo(self, request):

        try:

            if request.data["credito"] != 0:
                credito = Prestamos.objects.get(id = request.data["credito"])
                tasa_deuda = TasaParaCreditos.objects.get(id = request.data["tasa_deuda"])
                tasa_saldo = TasaParaCreditos.objects.get(id = request.data["tasa_saldo"])
                datos_refinanciamiento = prestamos_refinanciaminto_calculo(credito.id, tasa_deuda.valor_tasa, tasa_saldo.valor_tasa)

            else:
                credito = False
                datos_refinanciamiento = False

            tasa = float(TasaParaCreditos.objects.get(id = request.data["tasa"]).valor_tasa)
            monto_inicial = float(request.data['monto_incial']) + float(request.data['monto_extra'])
            periodo_gracia = int(request.data['peridos_gracia'])
            regimen = request.data['regimen']
            cantidad_cuotas = int(request.data['cantidad_cuotas'])
            
            try:
                datos_calculadora = prestamos_calculadora(tasa, monto_inicial, periodo_gracia, regimen, cantidad_cuotas)
            except:
                datos_calculadora = ["", "", ""]

            response = {}
            response["monto"] = round(datos_calculadora[0], 0)
            response["monto_cuota"] = round(datos_calculadora[1], 0)
            response["cuota"] = datos_calculadora[2]
            response["refinancimiento"] = datos_refinanciamiento,
            response["monto_original"] = round(datos_refinanciamiento['DeudaActual'] + datos_refinanciamiento['SaldoActual'], 0)
            response["simulacion"] = []

            if request.data['primera_cuota'] != "":
                primera_cuota = str(request.data['primera_cuota'])
                response["simulacion"] = simular_cuotas_prestamo(regimen, cantidad_cuotas, primera_cuota)

            return Response(response, status=status.HTTP_200_OK)

        except Exception as error:
            print(error.args)
            response = {"mensaje": "No encontrado"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def crear_prestamo(self, request):
        try:
                
            tasa = float(request.data['tasa'])
            monto_inicial = float(request.data['monto_incial'])
            periodo_gracia = int(request.data['peridos_gracia'])
            regimen = request.data['regimen']
            cantidad_cuotas = int(request.data['cantidad_cuotas'])

            string_cliente = request.data['cliente'].split("-")
            string_proveedor = request.data['proveedor'].split("-")
            cliente = Clientes.objects.get(id = string_cliente[0])
            proveedor = Proveedor.objects.get(id = string_proveedor[0])
            fecha = request.data['fecha']
            primera_cuota = request.data['primera_cuota']
            presupuesto_cliente = request.data['presupuesto_cliente']
            monto = prestamos_calculadora(tasa, monto_inicial, periodo_gracia, regimen, cantidad_cuotas)[0]

            crear_prestamo = prestamos_agregar_credito(cliente, proveedor, fecha, 
                primera_cuota, monto_inicial, presupuesto_cliente, 
                monto, cantidad_cuotas, regimen)

            response = {"message": "success"}

            return Response(response, status=status.HTTP_200_OK)

        except:

            response = {"mensaje": "No encontrado"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def crear_prestamo_refinanciado(self, request):

        try:
            string_proveedor = request.data['proveedor'].split("-")
            credito = Prestamos.objects.get(id = request.data["credito"])
            tasa_deuda = TasaParaCreditos.objects.get(id = request.data["tasa_deuda"]).valor_tasa
            tasa_saldo = TasaParaCreditos.objects.get(id = request.data["tasa_saldo"]).valor_tasa
            tasa = float(TasaParaCreditos.objects.get(id = request.data["tasa"]).valor_tasa)
            cliente = credito.cliente
            proveedor = Proveedor.objects.get(id = string_proveedor[0])
            fecha = request.data['fecha']
            primera_cuota = request.data['primera_cuota']
            monto_valor_actual = float(request.data['monto_inicial'])
            monto_extra = float(request.data['monto_extra'])
            monto_total = monto_valor_actual + monto_extra
            presupuesto_cliente = float(request.data['presupuesto_cliente'])
            periodo_gracia = int(request.data['peridos_gracia'])
            regimen = request.data['regimen']
            cantidad_cuotas = int(request.data['cantidad_cuotas'])
            monto_interes = prestamos_calculadora(tasa, monto_total, periodo_gracia, regimen, cantidad_cuotas)[0]
            
            old_prestamo = prestamos_cancelar_refinanciamiento(credito.id, tasa_deuda, tasa_saldo)
            nuevo_prestamo = prestamos_agregar_credito(cliente, proveedor, fecha, 
                primera_cuota, monto_total, presupuesto_cliente, 
                monto_interes, cantidad_cuotas, regimen, monto_valor_actual=monto_valor_actual)
                
            response = {"message": "success"}

            return Response(response, status=status.HTTP_200_OK)

        except:

            response = {"mensaje": "No encontrado"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def consulta_user(self, request):
        usuario = Clientes.objects.get(usuario__user__id = request.data['id'])
        prestamo = Prestamos.objects.filter(cliente = usuario).order_by("-id")
        response = {}
        
        if len(prestamo) > 0:
            prestamo = prestamo[0]
            response['monto_prestamo'] = round(prestamo.monto, 2),
            cuotas = CuotasPrestamo.objects.filter(prestamo = prestamo)
            cantidad_cuotas = len(cuotas)
            response['cantidad_cuotas'] = cantidad_cuotas
            cantidad_pendientes = len(cuotas.exclude(estado = "SI"))
            response['cantidad_pendientes'] = cantidad_pendientes
            proxima_cuota = cuotas.exclude(estado = "SI").exclude(estado = "PARCIAL").order_by("fecha")
            if len(proxima_cuota) > 0:
                proxima_cuota = proxima_cuota[0]
                response['monto_proxima_cuota'] = round((proxima_cuota.monto + proxima_cuota.monto_interes - proxima_cuota.monto_bonificado), 2)
                response['proximo_vencimiento'] = proxima_cuota.fecha
            else:
                response['monto_proxima_cuota'] = "Sin vencimiento"
                response['proximo_vencimiento'] = "Sin vencimiento"

        return Response(response, status=status.HTTP_200_OK)

