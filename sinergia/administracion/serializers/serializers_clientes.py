from rest_framework import serializers
from django.contrib.auth.models import User
from administracion.models import Clientes
from django.db import transaction


class ClientesSerialiazers(serializers.ModelSerializer):

    class Meta:
        model = Clientes
        fields = '__all__'