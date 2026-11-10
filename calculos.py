"""Funciones básicas del problema: extremismo, esfuerzo y aplicabilidad."""
import math

"""
 Funcion que calcula el esfuerzo de moderar a un agente
 El esfuerzo de moderar a un agente se calcula como el techo del valor absoluto de la opinión del agente multiplicado por (1 - receptividad) y por la influencia del agente.
 Esto se redondea a 9 decimales para evitar errores de precisión en los cálculos de punto flotante.
"""
def costo_agente(agente):
    return math.ceil(round(abs(agente.opinion) * (1 - agente.receptividad) * agente.influencia, 9))


"""
Funcion que calcule el aporte de la opinion de un agente al extremismo de la red social.
El aporte de un agente al extremismo se calcula como el cuadrado de la opinión del agente multiplicado 
por la influencia del agente.
"""
def aporte_agente(agente):
    return agente.opinion ** 2 * agente.influencia


"""
Funcion que calcula si una estrategia es aplicable a una red social. 
Valida si el tamaño de la estrategia es igual al número de agentes en la red social
"""
def _validar(red, estrategia):
    if len(estrategia) != red.n:
        raise ValueError(f"La estrategia tiene {len(estrategia)} elementos y la red {red.n} agentes")


"""
Funcion que calcula el extremismo de una red social. Si se pasa una estrategia, calcula el extremismo 
de la red social moderada, donde los agentes moderados aportan 0 al extremismo.
"""
def extremismo(red, estrategia=None):

    if estrategia is None:
        suma = sum(aporte_agente(a) for a in red.agentes)
    else:
        _validar(red, estrategia)
        suma = sum(aporte_agente(a) for a, e in zip(red.agentes, estrategia) if e == 0)
    return math.sqrt(suma) / red.n

"""
Funcion que calcula el esfuerzo de una estrategia en una red social.
El esfuerzo de una estrategia se calcula como la suma del esfuerzo de moderar 
a cada agente que está moderado en la estrategia (e_i = 1).

"""
def esfuerzo(red, estrategia):
    _validar(red, estrategia)
    return sum(costo_agente(a) for a, e in zip(red.agentes, estrategia) if e == 1)



"""
Funcion que valida si una estrategia es aplicable a una red social.
 Una estrategia es aplicable si el esfuerzo total de moderar a los agentes 
 seleccionados no supera el presupuesto máximo de la red social.
"""
def es_aplicable(red, estrategia):
    return esfuerzo(red, estrategia) <= red.r_max



def evaluar(red, estrategia):
    """Devuelve la tripleta (E, Esfuerzo, Ext) que deben retornar modexFB / modexV / modexPD."""
    return (list(estrategia), esfuerzo(red, estrategia), extremismo(red, estrategia))