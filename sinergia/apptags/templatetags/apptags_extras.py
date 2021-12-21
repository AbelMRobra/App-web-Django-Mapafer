from __future__ import unicode_literals
from django import template
from administracion.models import UserProfile

register = template.Library()

@register.simple_tag
def host():
    return "http://www.mapafer.online/"


@register.filter('has_rol')
def has_group(user, rol):
    """
    Verifica se este usuário pertence a un grupo
    """
    user_rol = UserProfile.objects.get(user = user).user_rol
    return True if user_rol ==  rol else False