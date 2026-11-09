"""Modelo de datos de ModEx y lectura de archivos de entrada."""
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Agente:
    opinion: int          # entero en [-100, 100]
    receptividad: float   # real en [0, 1]
    influencia: float     # real en [1, 3]


@dataclass(frozen=True, slots=True)
class RedSocial:
    agentes: tuple        # tuple[Agente, ...]; el agente i está en agentes[i]
    r_max: int            # presupuesto máximo de esfuerzo

    @property
    def n(self):
        return len(self.agentes)


def cargar_red_social(ruta):
    """Lee un archivo de entrada (formato 3.4.1 del enunciado) y devuelve una RedSocial."""
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = [l.strip() for l in f if l.strip()]   # ignora líneas vacías

    n = int(lineas[0])
    if len(lineas) != n + 2:
        raise ValueError(f"{ruta}: se esperaban {n + 2} líneas y hay {len(lineas)}")

    agentes = []
    for k, linea in enumerate(lineas[1:n + 1], start=1):
        partes = linea.replace(",", " ").split()
        if len(partes) != 3:
            raise ValueError(f"{ruta}, línea {k + 1}: se esperaban 3 valores: {linea!r}")
        agentes.append(Agente(int(partes[0]), float(partes[1]), float(partes[2])))

    return RedSocial(tuple(agentes), int(lineas[-1]))