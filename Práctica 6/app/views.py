from django.shortcuts import render, HttpResponse, redirect
from .models import *
# Create your views here.


def index(request):
	#si cambiamos la primera línea por mostrar_prestamos(), y los atributos en el index, muestra unos cuantos ya hechos de ejemplo.
	# Funciona pedir un prestamo nuevo
	data = mostrar_libros()
	return render(request, 'index.html', {"matriz": data})

def test_template(request):
    context = {}   # Aquí van la las variables para la plantilla
    return render(request,'test.html', context)

def nuevo_prestamo(request):
	if request.method == 'POST':
		registro = PrestamoForm(request.POST)
		if registro.is_valid():
			Nuevo_Prestamo(registro.cleaned_data['libro'], registro.cleaned_data['usuario'])
			return redirect('./')
	else:
		registro = PrestamoForm()
		return render(request, 'nuevo_prestamo.html', {'registro': registro})

def nuevo_libro(request):
	if request.method == 'POST':
		registro = LibroForm(request.POST)
		if registro.is_valid():
			Nuevo_Libro(registro.cleaned_data['titulo'], registro.cleaned_data['autor'])
			return redirect('./')
	else:
		registro = LibroForm()
		return render(request, 'nuevo_libro.html', {'registro': registro})