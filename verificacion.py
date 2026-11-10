from calculos import aporte_agente, costo_agente, es_aplicable, esfuerzo, extremismo


def calcular_desglose_costos(red, estrategia):
    total = 0
    detalles = []
    for i, (agente, e) in enumerate(zip(red.agentes, estrategia)):
        if e != 1:
            continue
        costo = costo_agente(agente)
        total += costo
        detalles.append(
            {
                "indice": i,
                "costo": costo,
                "formula": f"ceil(|{agente.opinion}|*(1-{agente.receptividad})*{agente.influencia}) = {costo}",
                "aporte": aporte_agente(agente),
            }
        )
    return total, detalles


def verificar_estrategia(red, estrategia, esfuerzo_reportado=None, ext_reportado=None):
    if len(estrategia) != red.n:
        raise ValueError(f"La estrategia tiene longitud {len(estrategia)} pero la red tiene {red.n} agentes.")

    ext_calc = extremismo(red, estrategia)
    esf_calc = esfuerzo(red, estrategia)
    aplicable = es_aplicable(red, estrategia)
    total_costos, detalles = calcular_desglose_costos(red, estrategia)

    lineas = []
    lineas.append("Verificación de la solución:")
    lineas.append(f"- Ext calculado: {ext_calc:.6f}")
    if ext_reportado is not None:
        lineas.append(f"- Ext reportado: {ext_reportado:.6f}")
        lineas.append(f"- Diferencia Extremismo: {abs(ext_calc - ext_reportado):.12f}")

    lineas.append(f"- Esfuerzo calculado: {esf_calc}")
    if esfuerzo_reportado is not None:
        lineas.append(f"- Esfuerzo reportado: {esfuerzo_reportado}")
        lineas.append(f"- Diferencia esfuerzo: {abs(esf_calc - esfuerzo_reportado)}")

    lineas.append(f"- Aplicable: {'Sí' if aplicable else 'No'}")
    lineas.append("Desglose de costos:")
    if not detalles:
        lineas.append("- No hay agentes moderados.")
    else:
        formula = " + ".join(d["formula"] for d in detalles)
        lineas.append(f"- {formula} = {total_costos}")
        lineas.append(f"- R_max = {red.r_max}")
        lineas.append(f"- ¿Cumple presupuesto? {'Sí' if total_costos <= red.r_max else 'No'}")

    return {
        "ext": ext_calc,
        "esfuerzo": esf_calc,
        "aplicable": aplicable,
        "desglose_total": total_costos,
        "detalles": detalles,
        "texto": "\n".join(lineas),
    }


def comparar_optimalidad(ext_algoritmo, ext_optimo):
    if ext_optimo == 0:
        return 0.0
    return ((ext_algoritmo - ext_optimo) / ext_optimo) * 100.0
