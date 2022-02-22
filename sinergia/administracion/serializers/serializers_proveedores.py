from rest_framework import serializers
from administracion.models import Proveedor

class ProveedorSerialiazers(serializers.ModelSerializer):

    class Meta:
        model = Proveedor
        fields = '__all__'