from flask import Flask
from flask import render_template
from random import randrange
import sys
import time

#####Funciones Auxiliares

##Ordenamientos

#Burbuja
def bubbleSort(arrayList):
    array = arrayList
    n = len(array)

    for i in range(n):
        for j in range(0, n-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]

    return array

#Mezcla
def mergeSort(myList):
    if len(myList) > 1:
        mid = len(myList) // 2
        left = myList[:mid]
        right = myList[mid:]

        # Recursive call on each half
        mergeSort(left)
        mergeSort(right)

        # Two iterators for traversing the two halves
        i = 0
        j = 0
        
        # Iterator for the main list
        k = 0
        
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
              # The value from the left half has been used
              myList[k] = left[i]
              # Move the iterator forward
              i += 1
            else:
                myList[k] = right[j]
                j += 1
            # Move to the next slot
            k += 1

        # For all the remaining values
        while i < len(left):
            myList[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            myList[k]=right[j]
            j += 1
            k += 1


#insercion
def insertionSort(arr): 
  
    # Traverse through 1 to len(arr) 
    for i in range(1, len(arr)): 
  
        key = arr[i] 
  
        # Move elements of arr[0..i-1], that are 
        # greater than key, to one position ahead 
        # of their current position 
        j = i-1
        while j >=0 and key < arr[j] : 
                arr[j+1] = arr[j] 
                j -= 1
        arr[j+1] = key

##Criba
def eratostenes(n):
    lista = []
    for i in range(2, n+1):
        lista.append(i)

    i=0    
    while(lista[i]*lista[i] <= n):
        # Mientras el cuadrado del elemento actual sea menor que el ultimo elemento
        for num in lista:
            if num <= lista[i]:
            # Cada iteracion del while hace que el for comience desde el primer elemento. 
            # Esto es para omitir los numeros primos ya encontrados
                continue
            elif num % lista[i] == 0:
            # Si un numero es divisible entre el elemento actual del while
            # de ser asi, entonces eliminarlo de la lista (esto altera la lista)
                lista.remove(num)
            else:
            # Si no es divisible, entonces omitirlo (no hacer nada)
                pass
        i += 1 # Incrementa al siguiente elemento de la lista (que ha sido alterada)

    return lista


##Fibonacci
def fibonacci(n):
    n = n-1
    list = [1,1,2]
    if n < 3:
        return list[n]
    else:
        for i in range(n-2):
            suma = list[1] + list[2]
            list[0] = list[1]
            list[1] = list[2]
            list[2] = suma
    return list[2]

##Corchetes anidados
def corchetes(list):
    contador = 0
    for x in list:
        if x == '[':
            contador = contador + 1
        else:
            contador = contador - 1
            if contador < 0:
                return False
    return contador==0


#####Los Routings
app = Flask(__name__)
          
@app.route('/')
def root():
    return render_template('index.html')


@app.route('/hello_world')
def hello_world():
    return 'Hello, World!'

@app.route('/ordena/<string:array>')
def ordena(array):
    
    arrayList = [int(x) for x in array.split(',')]
    ordenado_burbuja = arrayList.copy()
    ordenado_mezcla = arrayList.copy()
    ordenado_insercion = arrayList.copy()


    init = time.time()
    bubbleSort(ordenado_burbuja)
    tiempo_burbuja = time.time() - init


    init = time.time()
    mergeSort(ordenado_mezcla)
    tiempo_mezcla = time.time() - init

    init = time.time()
    insertionSort(ordenado_insercion)
    tiempo_insercion = time.time() - init

    return render_template("ordena.html", original=arrayList, burbuja=ordenado_burbuja, mezcla=ordenado_mezcla, insercion=ordenado_insercion, tiempo_burbuja=tiempo_burbuja, tiempo_mezcla=tiempo_mezcla, tiempo_insercion=tiempo_insercion)

@app.route('/criba/<int:num>')
def criba(num):
    return render_template("criba.html",cantidad=len(eratostenes(num)), original=eratostenes(num), num=num)

@app.route('/fibonacci/<int:num>')
def fibo(num):
    return render_template("fibonacci.html", posicion=num, resultado=fibonacci(num))

@app.route('/corchetes')
def corchete():
    n = randrange(20)
    list = ['[',']']
    array = []
    for i in range(n):
        array.append(list[randrange(len(list))])
    return render_template('corchetes.html',lista=array, boolean=corchetes(array))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

n = randrange(20)
list = ['[',']']
array = []
for i in range(n):
    array.append(list[randrange(len(list))])
print(array)
print(corchetes(array))
