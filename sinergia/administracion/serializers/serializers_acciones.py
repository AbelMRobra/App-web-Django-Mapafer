from rest_framework import serializers
from administracion.models import LogsAcciones


class LogsSerialiazers(serializers.ModelSerializer):

    class Meta:
        model = LogsAcciones
        fields = '__all__'