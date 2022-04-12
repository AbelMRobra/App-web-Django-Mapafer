from rest_framework import serializers
from administracion.models import MovimientoContable


class MovimientoContableSerialiazers(serializers.ModelSerializer):

    class Meta:
        model = MovimientoContable
        fields = '__all__'