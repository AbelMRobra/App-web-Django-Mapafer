from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

from administracion.models import Pagos
from administracion.serializers import serializers_pagos

class PagosViewset(viewsets.ModelViewSet):

    queryset = Pagos.objects.all()
    serializer_class = serializers_pagos.PagosSerializers
    permission_classes = (IsAuthenticated,)
