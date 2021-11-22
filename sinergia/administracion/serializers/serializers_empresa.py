from rest_framework import serializers
from administracion.models import Empresa, ContactosEmpresa, ContactosEmpresa


class EmpresaSerializers(serializers.ModelSerializer):

    class Meta:
        model = Empresa
        fields = ('__all__')

class ContactosEmpresaSerializers(serializers.ModelSerializer):

    class Meta:
        model = ContactosEmpresa
        fields = ('__all__')

