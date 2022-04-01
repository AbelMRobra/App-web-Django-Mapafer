import datetime
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from administracion.serializers import serializers_acciones
from administracion.models import LogsAcciones, Prestamos
from rest_framework.decorators import action
from rest_framework.response import Response
from ..funciones import f_prestamos

class AccionesViewset(viewsets.ModelViewSet):

    queryset = LogsAcciones.objects.all()
    serializer_class = serializers_acciones.LogsSerialiazers
    permission_classes = (AllowAny,)

    @action(methods=['GET'], detail=False)
    def consulta_dia(self, request):
        
        try:
            query_diaria = LogsAcciones.objects.filter(dia = datetime.date.today())
            
            if len(query_diaria) > 0:
                response = {'message': 'Realizado'}
            else:
                response = {'message': 'Pendiente'}

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:

            response = {"mensaje": f"Error inesperado: {e.args}"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['GET'], detail=False)
    def revisar_clientes(self, request):
        
        try:
            query_prestamos = Prestamos.objects.all()

            for prestamo in query_prestamos:
                f_prestamos.prestamos_cuotas_pagos(prestamo.id)

            
            log = LogsAcciones.objects.create(
                fecha = datetime.datetime.now(),
                dia = datetime.date.today(),
                accion = "Sincronización de creditos diaria",
                resultado = "Realizada con exito"
            )
            
            response = {'message': 'Realizado con exito'}
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            response = {"mensaje": f"Error inesperado: {e.args}"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
