from django.db.models import Sum
from django.shortcuts import render
from administracion.models import PagosProveedores, Pagos, MovimientoContable

def principal_caja(request):
    context = {}
    context['pagos'] = Pagos.objects.all().values("fecha").order_by("fecha").annotate(total_monto=Sum('monto'))
    context['pagos_proveedores'] = PagosProveedores.objects.all().values("fecha").order_by("fecha").annotate(total_monto=Sum('monto'))
    context['movimientos'] = MovimientoContable.objects.all()

    return render(request, "caja/caja_principal.html", context)