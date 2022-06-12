# mi_aplicacion/models.py
from django.db import models
from django.utils import timezone
from django import forms


class Libro(models.Model):
  titulo = models.CharField(max_length=200, primary_key=True)
  autor  = models.CharField(max_length=100)


class Prestamo(models.Model):
  libro   = models.ForeignKey(Libro, on_delete=models.CASCADE)
  fecha   = models.DateField(default=timezone.now)
  usuario = models.CharField(max_length=100)


def mostrar_libros():
  return Libro.objects.all()

def mostrar_prestamos():
  return Prestamo.objects.all()

#MODIFICACIONES BD
def Nuevo_Libro(titulo, autor):
  	libro = Libro(titulo, autor)
  	libro.save()


def Nuevo_Prestamo(libro, usuario):
	prestamo = Prestamo(libro=Libro.objects.get(titulo=libro), usuario=usuario)
	prestamo.save()

  

#FORMULARIOS

class LibroForm(forms.Form):
	titulo = forms.CharField(label='Titulo:', max_length=100)
	autor = forms.CharField(label='Autor:', max_length=60)


class PrestamoForm(forms.Form):
	libro = forms.CharField()
	usuario = forms.CharField(max_length=100)

