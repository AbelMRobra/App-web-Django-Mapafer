from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from administracion.serializers import serializers_movimiento
from administracion.models import MovimientoContable


class MovimientoContableViewset(viewsets.ModelViewSet):

    queryset = MovimientoContable.objects.all()
    serializer_class = serializers_movimiento.MovimientoContableSerialiazers
    permission_classes = (AllowAny,)

