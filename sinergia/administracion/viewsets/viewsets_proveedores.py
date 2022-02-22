from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from administracion.serializers import serializers_proveedores
from administracion.models import Proveedor



class ProveedorViewset(viewsets.ModelViewSet):

    queryset = Proveedor.objects.all()
    serializer_class = serializers_proveedores.ProveedorSerialiazers
    permission_classes = (IsAuthenticated,)

