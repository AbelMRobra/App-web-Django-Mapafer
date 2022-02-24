from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.response import Response
from django.db import transaction
from administracion.models import TasaParaCreditos
from administracion.serializers import serializers_tasas


class TasasViewset(viewsets.GenericViewSet, mixins.UpdateModelMixin):

    queryset = TasaParaCreditos.objects.all()
    serializer_class = serializers_tasas.TasasSerializer
    permission_classes = (IsAuthenticated,)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        tasa_1 = TasaParaCreditos.objects.get(id = 2)
        tasa_1.valor_tasa = instance*1.2
        tasa_1.save()

        tasa_2 = TasaParaCreditos.objects.get(id = 3)
        tasa_2.valor_tasa = instance*1.1
        tasa_2.save()

        tasa_3 = TasaParaCreditos.objects.get(id = 4)
        tasa_3.valor_tasa = instance*0.9
        tasa_3.save()

        tasa_4 = TasaParaCreditos.objects.get(id = 5)
        tasa_4.valor_tasa = instance*0.8
        tasa_4.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

