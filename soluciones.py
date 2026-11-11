"""
En el ambiente de programaci´on de su preferencia, un programa que contenga una funci´on por cada
una de las soluciones dise˜nadas y analizadas (fuerza bruta, voraz y programaci´on din´amica). Cada
funci´on recibe una red social RS y devuelve una tripleta (E, Esfuerzo(RS, E), Ext(Mod(RS, E)))
que contiene E, la respuesta al problema, y el valor del esfuerzo de esa soluci´on y del extremismo
de la red moderada. Esas funciones en su c´odigo deben llamarse modexFB, modexV y modexPD.

"""

from calculos import costo_agente, aporte_agente, evaluar

"""
Funcion que implementa la fuerza bruta para resolver el problema de ModEx. 
Recorre todas las estrategias posibles (2^n) con un arbol de decisiones, 
en cada nivel decide si moderar o no al agente i.
Al final devuelve la mejor estrategia encontrada.

"""
def modexFB(red):
    n = red.n
    costos = [costo_agente(a) for a in red.agentes]
    aportes = [aporte_agente(a) for a in red.agentes]
 
    E = [0] * n   # estrategia en construcción
    mejor = {"suma": float("inf"), "E": None}
 
    def explorar(i, esf, suma):
        # esf  = esfuerzo acumulado de los agentes ya moderados
        # suma = sum(o^2 * inf) aporte en el extremismo de los agentes decididos que NO se moderan
        if i == n:   # hoja: estrategia completa
            if esf <= red.r_max and suma < mejor["suma"]:
                mejor["suma"] = suma
                mejor["E"] = E.copy()
            return
        E[i] = 1     # rama 1: moderar al agente i
        explorar(i + 1, esf + costos[i], suma)
        E[i] = 0      # rama 0: no moderarlo al agente i
        explorar(i + 1, esf, suma + aportes[i])
 
    explorar(0, 0, 0)
    return evaluar(red, mejor["E"])   # Devuelve la tripleta (E, Esfuerzo(RS, E), Ext(Mod(RS, E))

## Funcion que implementa el algoritmo voraz para resolver el problema de ModEx. No garantiza la mejor solución, pero es eficiente y rápida.
def modexV(red):
    n = red.n
    costos = [costo_agente(a) for a in red.agentes]
    aportes = [aporte_agente(a) for a in red.agentes]

    E = [0] * n   # estrategia en construcción

    def razon(i):
        return float("inf") if costos[i] == 0 else aportes[i] / costos[i]
 
    razones_ordenadas = sorted(range(n), key=razon, reverse=True)
    
    # Aplicar el algoritmo voraz
    esfuerzo_total = 0
    for i in razones_ordenadas:
        if esfuerzo_total + costos[i] <= red.r_max:  # si no cabe, se salta y se sigue con el siguiente
            E[i] = 1
            esfuerzo_total += costos[i]

    return evaluar(red, E)   # Devuelve la tripleta (E, Esfuerzo(RS, E), Ext(Mod(RS, E))


def modexPD(red):
    n, R = red.n, red.r_max
    c = [costo_agente(a) for a in red.agentes]
    v = [aporte_agente(a) for a in red.agentes]

    # M[i][j] = max extremismo eliminado con los agentes 0..i-1 y presupuesto j
    M = [[0.0] * (R + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        ci, vi = c[i-1], v[i-1]
        for j in range(R + 1):
            M[i][j] = M[i-1][j]                      # no moderar al agente i-1
            if ci <= j and M[i-1][j-ci] + vi > M[i][j]:
                M[i][j] = M[i-1][j-ci] + vi          # moderarlo

    # Recuperar E recorriendo la tabla hacia atrás
    E = [0] * n
    j = R
    for i in range(n, 0, -1):
        if M[i][j] != M[i-1][j]:    # el valor cambió => el agente i-1 fue moderado
            E[i-1] = 1
            j -= c[i-1]
    return evaluar(red, E)
