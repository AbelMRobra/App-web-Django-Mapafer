from rest_framework import serializers
from administracion.models import Pagos

class PagosSerializers(serializers.ModelSerializer):

    class Meta:
        model = Pagos
        fields = ('__all__')