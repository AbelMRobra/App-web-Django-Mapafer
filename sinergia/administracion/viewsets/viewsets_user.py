from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import transaction
from administracion.serializers import serializers_user
from administracion.models import UserProfile


class UserViewset(viewsets.ModelViewSet):

    queryset = UserProfile.objects.all()
    serializer_class = serializers_user.UserProfileSerialiazers
    permission_classes = (AllowAny,)

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        data_profile = request.data['user_rol']
        request.data.pop('user_rol')
        data_user = request.data
        serializer_user = serializers_user.UserSerializers(data = data_user)
        serializer_user.is_valid(raise_exception=True)
        user = serializer_user.save()
        print(data_profile)
        user_profile = UserProfile.objects.create(user = user, user_rol = data_profile)
        response = {'message' : 'Create Success'}

        return Response(response, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"])
    def editar_usuario(self, request, pk):
        try:

            user_profile = UserProfile.objects.get(pk = pk)
            user_profile.user_rol = request.data['user_rol']
            user_profile.save()

            user = User.objects.get(pk = user_profile.user.pk)
            user.username = request.data['username']
            user.email = request.data['email']
            user.save()
 

            response = {'message' : 'Upload Success'}

            return Response(response, status=status.HTTP_200_OK)

        except:

            response = {'message': 'Not found'}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

