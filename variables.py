# variables
saludo = "Hola"

# Python es tipado Dinamico: significa que no tenemos que definir el dato pero si se quiere ser mas especifico si se puede definir
saludo:str = "Hola"
numero:int = 25
booleano:bool = True
flotante:float = 4.5

# Lista,tuplas,diccionarios,conjuntos
list = ["Hola", 34, 28.9, False] # son dinamicas,son mutables:se pueden modificar:agregar,quitar

tuple = () # No es mutable, no es dinamica

diccionario = {"saludo":"Hola mundo","Grados celcius":"21.3","turno":"30","Disponible":"False"}

conjunto = {1,2,3,4,5,6,7,8,9} # no es mutable, no se puede modificar, en la impresion puede salir en desorden

print (type(saludo))

# Casting de variables: es cuando decido convertir un valor a otro, en otros lenguajes es parseo

edad = "23"

print (type(edad))

edad = int ("23")
print (type(edad))

nombre = input ("Escriba su nombre:")
edad = int(input("Ingrese su edad:"))
print ("Nombre:  ", nombre)  # Concatenacion, 
print ("Nombre: "+ nombre) # solo para string 
print (f"Nombre {nombre}") # concatenacion FORMATO.
