"""Funciones básicas del problema: extremismo, esfuerzo y aplicabilidad."""
import math


def costo_agente(agente):
    """Esfuerzo de moderar a UN agente: ceil(|o| * (1 - r) * inf).
    El round(..., 9) evita que errores de float (p.ej. 48.00000000000001) suban el techo."""
    return math.ceil(round(abs(agente.opinion) * (1 - agente.receptividad) * agente.influencia, 9))


def aporte_agente(agente):
    """Lo que el agente suma dentro de la raíz del extremismo: o^2 * inf."""
    return agente.opinion ** 2 * agente.influencia


def _validar(red, estrategia):
    if len(estrategia) != red.n:
        raise ValueError(f"La estrategia tiene {len(estrategia)} elementos y la red {red.n} agentes")


def extremismo(red, estrategia=None):
    """Ext(RS) = sqrt(sum(o_i^2 * inf_i)) / n.
    Si se pasa una estrategia, calcula Ext(Mod(RS, E)): los agentes moderados aportan 0."""
    if estrategia is None:
        suma = sum(aporte_agente(a) for a in red.agentes)
    else:
        _validar(red, estrategia)
        suma = sum(aporte_agente(a) for a, e in zip(red.agentes, estrategia) if e == 0)
    return math.sqrt(suma) / red.n


def esfuerzo(red, estrategia):
    """Esfuerzo(RS, E): suma de costo_agente de los agentes con e_i = 1."""
    _validar(red, estrategia)
    return sum(costo_agente(a) for a, e in zip(red.agentes, estrategia) if e == 1)


def es_aplicable(red, estrategia):
    return esfuerzo(red, estrategia) <= red.r_max


def evaluar(red, estrategia):
    """Devuelve la tripleta (E, Esfuerzo, Ext) que deben retornar modexFB / modexV / modexPD."""
    return (list(estrategia), esfuerzo(red, estrategia), extremismo(red, estrategia))