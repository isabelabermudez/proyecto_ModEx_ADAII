import os
from red_social import cargar_red_social
from calculos import extremismo, esfuerzo, es_aplicable
from soluciones import modexFB

CARPETA_PRUEBAS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Bateria de pruebas")


def ruta_prueba(numero):
    return os.path.join(CARPETA_PRUEBAS, f"Prueba{numero}.txt")


def probar_prueba1():
    """Verificación manual con la primera prueba."""
    red = cargar_red_social(ruta_prueba(1))
    print(f"Prueba 1: n={red.n}, R_max={red.r_max}")
    print("Extremismo sin moderar:", extremismo(red))

    estrategia = [1, 0, 0, 0, 0]          # moderar solo al agente 0
    print("Estrategia:", estrategia)
    print("Esfuerzo:", esfuerzo(red, estrategia), "| aplicable:", es_aplicable(red, estrategia))
    print("Extremismo moderado:", extremismo(red, estrategia))


def menu():
    while True:
        entrada = input("\nNúmero de prueba (1-35, Enter para salir): ").strip()
        if not entrada:
            break
        try:
            red = cargar_red_social(ruta_prueba(int(entrada)))
        except ValueError:
            print("Escribe un número entero.")
            continue
        except FileNotFoundError:
            print("Esa prueba no existe.")
            continue
        print(f"Red cargada: n={red.n}, R_max={red.r_max}")
        print(f"Extremismo de la red: {extremismo(red):.4f}")
        print("Resolviendo con fuerza bruta...")
        E, Esf, Ext = modexFB(red) 
        print(f"Fuerza bruta: E={E}, Esfuerzo={Esf}, Extremismo={Ext:.4f}")


def main():
    probar_prueba1()
    menu()


if __name__ == "__main__":
    main()