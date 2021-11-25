from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

from administracion.models import Prestamos
from administracion.serializers import serializers_prestamos

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
