from django.db.models import fields
from rest_framework import serializers
from administracion.models import TasaParaCreditos

class TasasSerializer(serializers.ModelSerializer):

    class Meta:
        model = TasaParaCreditos
        fields = ('__all__')