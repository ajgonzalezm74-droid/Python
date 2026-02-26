#-- Mini aventurero



print("Bienvenido a las mazmorra de Python")
nombre=input("¿Como se llama tu Heroe favorito?")
puntos_vida=10

print(f"\nHola {nombre}, tienes {puntos_vida} puntos de vida")

jugando=True
while jugando:
    print("\nTe encuentra frente a dos puetas, [1] Izquierda o [2] Derecha" )
    opcion=input("¿Cueal Eliges?, (escribe 1 o 2 o 's' para terminar):")

    if opcion == "1":
        print("Eleciion equivocada, pierdes 4 puntos de vida")
        puntos_vida -=4
    elif opcion == "2":
            print("eleccion correcta ganas 6 puntos de vida")
            puntos_vida +=6
    elif opcion.lower()=="s":
            print("Garcias por jugar")
            break
    else:
            print("opcion no valida")

    print(f"puntos de Vida: {puntos_vida}")

    if puntos_vida <= 0:
                print("¡Oh no! Te has quedado sin vida. Fin del juego.")
                jugando = False
 