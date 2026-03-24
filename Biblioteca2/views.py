# views.py
from django.shortcuts import render

def pagina_inicio(request):
    # Aquí podrías poner lógica (ej: contar cuántos libros hay)
    return render(request, 'inicio.html')