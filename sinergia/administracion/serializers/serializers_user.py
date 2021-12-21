from rest_framework import serializers
from django.contrib.auth.models import User
from administracion.models import UserProfile
from django.db import transaction


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):

        user = User.objects.create_user(**validated_data)       
        return user


class UserProfileSerialiazers(serializers.ModelSerializer):

    user = UserSerializers()

    class Meta:

        model = UserProfile
        fields = ('id', 'user', 'user_rol')





    



