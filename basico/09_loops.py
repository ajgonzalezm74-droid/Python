### Loops ###

# While

my_condition = 0

while my_condition < 10:
    print(my_condition)
    my_condition += 2
else:  # Es opcional
    print("Mi condición es mayor o igual que 10")

print("La ejecución continúa")

while my_condition < 20:
    my_condition += 1
    if my_condition == 15:
        print("Se detiene la ejecución")
        break
    print(my_condition)

print("La ejecución continúa")

# For

for i in range(0, 5):
    print(i)


for i in "Python":
    print(i)

#¿pero cómo se yo si algo es iterable o no?.
#Bien fácil, con la siguiente función isinstance() podemos saberlo
# True significa que es iterable y False que no lo es.

from collections.abc import Iterable
lista = [1, 2, 3, 4]
cadena = "Python"
numero = 10
print(isinstance(lista, Iterable))  #True
print(isinstance(cadena, Iterable)) #True
print(isinstance(numero, Iterable)) #False

#Por lo tanto las listas y las cadenas son iterables, pero numero, que es un entero no lo es.
#De hecho el error sería TypeError: int' object is not iterable.

#verificamos y ejecutamos 
objetos = [lista, cadena, numero]

for obj in objetos:
    if isinstance(obj,Iterable):
        print(f"\nRecoriendo:{obj}")

        for elemento in obj:
            print(f"\n{obj}")
    else:
        print(f"\n{obj} no se puede recorrer (no es iterable).") 

        
# Para entender los iteradores, es importante conocer la función iter() en Python
lista = [5, 6, 3, 2]
it = iter(lista)
print(it)       #<list_iterator object at 0x106243828>
print(type(it)) #<class 'list_iterator'>
#Vemos que al imprimir it es un iterador, de la clase list_iterator.

#Esta variable iteradora, hace referencia a la lista original 
# y nos permite acceder a sus elementos con la función next().
#Cada vez que llamamos a next() sobre it, nos devuelve el siguiente elemento de la lista original. 

print(next(it))

print(next(it))

print(next(it))

'''Para saber mas: Existen otros iteradores para diferentes clases:

str_iterator para cadenas
list_iterator para sets.
tuple_iterator para tuplas.
set_iterator para sets.
dict_keyiterator para diccionarios.'''


my_list = [35, 24, 62, 52, 30, 30, 17]

for element in my_list:
    print(element)

my_tuple = (35, 1.77, "Brais", "Moure", "Brais")

for element in my_tuple:
    print(element)

my_set = {"Brais", "Moure", 35}

for element in my_set:
    print(element)

my_dict = {"Nombre": "Brais", "Apellido": "Moure", "Edad": 35, 1: "Python"}

for element in my_dict:
    print(element)
    if element == "Edad":
        break
else:
    print("El bucle for para el diccionario ha finalizado")

print("La ejecución continúa")

for element in my_dict:
    print(element)
    if element == "Edad":
        continue
    print("Se ejecuta")
else:
    print("El bluce for para diccionario ha finalizado")