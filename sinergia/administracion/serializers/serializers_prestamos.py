from rest_framework import serializers
from administracion.models import Prestamos

class PrestamosSerializers(serializers.ModelSerializer):

    class Meta:
        model = Prestamos
        fields = ('__all__')