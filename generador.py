import random

from red_social import Agente, RedSocial


def generar_caso(
    tipo,
    n,
    opinion_min=-100,
    opinion_max=100,
    receptividad_min=0.0,
    receptividad_max=1.0,
    influencia_min=1.0,
    influencia_max=3.0,
    r_max=None,
    seed=None,
):
    """Genera una instancia de RedSocial según un tipo de caso.

    Tipos soportados:
    - aleatorio_uniforme
    - dificil_para_voraz
    - facil
    """
    if n <= 0:
        raise ValueError("n debe ser un entero positivo.")

    rng = random.Random(seed)

    if tipo == "aleatorio_uniforme":
        agentes = []
        for _ in range(n):
            opinion = rng.randint(int(opinion_min), int(opinion_max))
            receptividad = rng.uniform(receptividad_min, receptividad_max)
            influencia = rng.uniform(influencia_min, influencia_max)
            agentes.append(Agente(opinion, receptividad, influencia))
        if r_max is None:
            r_max = max(1, int(sum(abs(a.opinion) for a in agentes) * 0.35))
        return RedSocial(tuple(agentes), int(r_max))

    if tipo == "facil":
        agentes = []
        for _ in range(n):
            opinion = rng.randint(-20, 20)
            receptividad = rng.uniform(0.7, 1.0)
            influencia = rng.uniform(1.0, 1.8)
            agentes.append(Agente(opinion, receptividad, influencia))
        if r_max is None:
            r_max = 10000
        return RedSocial(tuple(agentes), int(r_max))

    if tipo == "dificil_para_voraz":
        agentes = []
        for i in range(n):
            if i % 5 == 0:
                opinion = rng.randint(70, 100)
                receptividad = rng.uniform(0.05, 0.25)
                influencia = rng.uniform(2.0, 3.0)
            elif i % 3 == 0:
                opinion = rng.randint(20, 45)
                receptividad = rng.uniform(0.8, 0.95)
                influencia = rng.uniform(1.1, 2.0)
            else:
                opinion = rng.randint(-60, 60)
                receptividad = rng.uniform(0.3, 0.9)
                influencia = rng.uniform(1.0, 3.0)
            agentes.append(Agente(opinion, receptividad, influencia))
        if r_max is None:
            r_max = max(1, int(sum(abs(a.opinion) for a in agentes) * 0.25))
        return RedSocial(tuple(agentes), int(r_max))

    raise ValueError(f"Tipo de caso no soportado: {tipo}")
