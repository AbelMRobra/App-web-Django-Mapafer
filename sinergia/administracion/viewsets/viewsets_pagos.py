from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

from administracion.models import Pagos
from administracion.serializers import serializers_pagos

from ..funciones.f_prestamos import *

class PagosViewset(viewsets.ModelViewSet):

    queryset = Pagos.objects.all()
    serializer_class = serializers_pagos.PagosSerializers
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        prestamos_cuotas_pagos(request.data['prestamo'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    