from django.shortcuts import render

def usuarios_panel(request):

    return render(request, "usuarios/usuarios_principal.html")

