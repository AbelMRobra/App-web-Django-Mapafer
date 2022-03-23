from django.shortcuts import render


def principal_caja(request):
    context = {}

    return render(request, "caja/caja_principal.html", context)