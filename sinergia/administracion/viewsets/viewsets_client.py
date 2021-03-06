from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.contrib.auth.models import User
from administracion.serializers import serializers_user, serializers_clientes
from administracion.models import Clientes, Empresa, UserProfile
from rest_framework.settings import api_settings


class ClientViewset(viewsets.ModelViewSet):

    queryset = Clientes.objects.all()
    serializer_class = serializers_clientes.ClientesSerialiazers
    permission_classes = (AllowAny,)

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        try:
            # Creamos primero el cliente
            request.data['empresa'] = Empresa.objects.get(nombre = request.data['empresa']).id
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
        
        except Exception as error:
            message = ""
            for key, value in error.args[0].items():
                error_causa = value[0]
                message += str(key).capitalize() + ": " + error_causa + "" +"\n"
            
            response = {'message': message}
            
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Luego creamos el usuario
            request.data['first_name'] = request.data['nombre']
            request.data['last_name'] = request.data['apellido']
            serializer_user = serializers_user.UserSerializers(data=request.data)
            serializer_user.is_valid(raise_exception=True)
            self.perform_create(serializer_user)

        except:
            response = {'message': 'No se pudo crear el usuario, revise los usuarios activos'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Creamos el perfil del usuario
            user_profile = UserProfile.objects.create(user_rol = "USER", user = User.objects.get(id = serializer_user.data['id']))
            cliente = Clientes.objects.get(id = serializer.data['id'])
            cliente.usuario = user_profile
            cliente.save()

        except:
            response = {'message': 'No se pudo crear el perfil'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        


