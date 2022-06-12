#model de pyhton
from pickleshare import *
#Funciones Practica3

def iniciarBD():
    db = PickleShareDB('/data/users')

    ##Introduccion de usuarios iniciales:

    db['pepe'] = dict()
    db['pepe']['pass'] = '1234'
    db['pepe'] = db['pepe']
    db['paco'] = dict()
    db['paco']['pass'] = '1234'
    db['paco'] = db['paco']
    



def credenciales_correctas(name, passw):
    db = PickleShareDB('/data/users')
    if name in db.keys():
        return db[name]['pass'] == passw
    else:
        return False

def adduser(name, passwd):
    db = PickleShareDB('/data/users')
    if name in db.keys():
        return False
    else:
        db[name] = dict()
        db[name]['pass'] = passwd
        db[name] = db[name]
        return True

def edituser(name, name2, passwd):
    db = PickleShareDB('/data/users')
    if name in db.keys() and db[name]['pass'] == passwd:
        db[name2] = dict()
        db[name2]['pass'] = passwd
        db[name].clear()
        del db[name]
        return True
    else:
        return False

def removeuser(name):
    db = PickleShareDB('/data/users')
    if name in db.keys(): 
        db[name].clear()
        del db[name]     
        return True
    else:
        return False

def changepass(name, pass2):
    db = PickleShareDB('/data/users')
    db[name]['pass'] = pass2
    db[name] = db[name]

def list_users():
    db = PickleShareDB('/data/users')
    return db.keys()

#####Funciones Practica2

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
        if x == "[":
            contador = contador + 1
        else:
            contador = contador - 1
            if contador < 0:
                return False
    return contador==0
