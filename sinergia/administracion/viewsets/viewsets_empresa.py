from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes

from administracion.models import Empresa, ContactosEmpresa
from administracion.serializers import serializers_empresa

class ContactosEmpresaViewset(viewsets.ModelViewSet):

    queryset = ContactosEmpresa.objects.all()
    serializer_class = serializers_empresa.ContactosEmpresaSerializers
    permission_classes = (AllowAny,)


class EmpresaViewset(viewsets.ModelViewSet):

    queryset = Empresa.objects.all()
    serializer_class = serializers_empresa.EmpresaSerializers
    permission_classes = (AllowAny,)

    @action(methods=['POST'], detail=True)

    def editar_datos(self, request, pk):
        
        try:
            empresa = Empresa.objects.get(id = pk)
            empresa.rubro = request.data["rubro"]
            empresa.direccion = request.data["direccion"]
            empresa.telefono = request.data["telefono"]
            empresa.save()

            response = {"mensaje": f"Empresa editada!",
            "rubro": empresa.rubro, "direccion": empresa.direccion, "telefono": empresa.telefono}
            return Response(response, status=status.HTTP_202_ACCEPTED)

        except:

            response = {"mensaje": "Error inesperado"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)