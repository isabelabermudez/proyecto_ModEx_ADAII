import csv


def formatear_float(valor):
    texto = f"{valor:.12f}".rstrip("0").rstrip(".")
    return texto if texto else "0"


def guardar_entrada(red, ruta):
    """Guarda una red social en el formato de entrada del enunciado."""
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"{red.n}\n")
        for agente in red.agentes:
            f.write(f"{agente.opinion}, {agente.receptividad}, {agente.influencia}\n")
        f.write(f"{red.r_max}\n")


def guardar_salida(ruta, ext, esfuerzo_total, estrategia):
    """Guarda la salida en el formato exigido por el proyecto."""
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f"{formatear_float(ext)}\n")
        f.write(f"{esfuerzo_total}\n")
        for bit in estrategia:
            f.write(f"{bit}\n")


def leer_salida(ruta):
    """Lee una salida y devuelve (ext, esfuerzo, estrategia)."""
    with open(ruta, "r", encoding="utf-8") as f:
        lineas = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    if len(lineas) < 2:
        raise ValueError("El archivo de salida está incompleto.")

    try:
        ext = float(lineas[0])
    except ValueError as exc:
        raise ValueError(f"Extremismo inválido en la salida: {lineas[0]!r}") from exc

    try:
        esfuerzo_total = int(lineas[1])
    except ValueError as exc:
        raise ValueError(f"Esfuerzo inválido en la salida: {lineas[1]!r}") from exc

    estrategia = []
    for idx, linea in enumerate(lineas[2:]):
        try:
            bit = int(linea)
        except ValueError as exc:
            raise ValueError(f"Valor no válido en mod_{idx}: {linea!r}") from exc
        if bit not in (0, 1):
            raise ValueError(f"mod_{idx} debe ser 0 o 1, llegó a {bit}")
        estrategia.append(bit)

    return ext, esfuerzo_total, estrategia


def guardar_csv(ruta, cabeceras, filas):
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(cabeceras)
        writer.writerows(filas)
