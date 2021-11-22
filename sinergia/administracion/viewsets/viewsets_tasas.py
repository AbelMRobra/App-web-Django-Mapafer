from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

from administracion.models import TasaParaCreditos
from administracion.serializers import serializers_tasas


class TasasViewset(viewsets.ModelViewSet):

    queryset = TasaParaCreditos.objects.all()
    serializer_class = serializers_tasas.TasasSerializer
    permission_classes = (AllowAny,)

