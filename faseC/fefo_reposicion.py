#fase c · reserva fefo (first expired, first out) y regla de punto de pedido
from datetime import date

#lectura y validación de lotes: (código, fecha_vencimiento, disponible)
def validar_lotes(lotes):
    for codigo, venc, disp in lotes:
        if not isinstance(venc, date):
            raise ValueError(f"lote {codigo}: fecha inválida")
        if not isinstance(disp, int) or disp < 0:
            raise ValueError(f"lote {codigo}: disponible inválido ({disp})")

#fefo: excluye vencidos y sin stock, ordena por (vencimiento, código) y reserva en ese orden
#politica = "parcial" reserva lo que alcance; "rechazar" no reserva nada si no cubre todo
def reservar_fefo(lotes, cantidad, hoy, politica="parcial"):
    validar_lotes(lotes)
    if not isinstance(cantidad, int) or cantidad <= 0:
        raise ValueError("la cantidad pedida debe ser un entero positivo")
    if politica not in ("parcial", "rechazar"):
        raise ValueError("política desconocida")
    #un lote que vence hoy se considera vencido
    candidatos = [l for l in lotes if l[1] > hoy and l[2] > 0]          #o(l)
    candidatos.sort(key=lambda l: (l[1], l[0]))                         #o(l log l); desempate por código
    plan, pendiente = [], cantidad
    for codigo, venc, disp in candidatos:                               #o(l)
        if pendiente == 0:
            break                       #termina: pendiente baja en cada lote usado o se acaban los lotes
        tomar = min(pendiente, disp)
        plan.append((codigo, venc.isoformat(), tomar))
        pendiente -= tomar
    if pendiente == 0:
        return {"estado": "completo", "plan": plan, "faltante": 0}
    if politica == "rechazar":
        return {"estado": "rechazado", "plan": [], "faltante": pendiente}
    return {"estado": "stock insuficiente", "plan": plan, "faltante": pendiente}

#reposición: posición = disponible + en_orden - reservado; si posición <= mínimo sugiere objetivo - posición
#como en_orden ya suma las órdenes abiertas, una segunda corrida no vuelve a pedir lo mismo
def sugerir_reposicion(skus):
    sugerencias = {}
    for sku, d in skus.items():                                         #o(p)
        for campo in ("disponible", "en_orden", "reservado", "minimo", "objetivo"):
            if not isinstance(d.get(campo), int) or d[campo] < 0:
                raise ValueError(f"{sku}: campo {campo} inválido")
        if d["objetivo"] < d["minimo"]:
            raise ValueError(f"{sku}: el objetivo no puede ser menor que el mínimo")
        posicion = d["disponible"] + d["en_orden"] - d["reservado"]
        sugerencia = max(0, d["objetivo"] - posicion) if posicion <= d["minimo"] else 0
        sugerencias[sku] = {"posicion": posicion, "sugerencia": sugerencia}
    return sugerencias

#presentación y pruebas
if __name__ == "__main__":
    hoy = date(2026, 11, 24)
    lotes = [("L-104", date(2026, 12, 20), 30),
             ("L-101", date(2026, 12, 5), 10),
             ("L-103", date(2026, 12, 5), 15),   #empata con l-101: decide el código
             ("L-099", date(2026, 11, 20), 50),  #vencido: se excluye
             ("L-102", date(2026, 11, 30), 0)]   #sin stock: se excluye

    print("FEFO · pedido de 30 unidades")
    r1 = reservar_fefo(lotes, 30, hoy)
    for paso in r1["plan"]:
        print("  ", paso)
    print("  ", r1["estado"], "| faltante:", r1["faltante"])

    print("FEFO · pedido de 70 (no alcanza: hay 55 elegibles)")
    r2 = reservar_fefo(lotes, 70, hoy)
    print("   parcial ->", r2["estado"], r2["plan"], "faltante", r2["faltante"])
    r3 = reservar_fefo(lotes, 70, hoy, politica="rechazar")
    print("   rechazar ->", r3["estado"], "faltante", r3["faltante"])

    print("FEFO · lote que vence hoy (límite)")
    r4 = reservar_fefo([("L-200", hoy, 10)], 5, hoy)
    print("  ", r4["estado"], "faltante", r4["faltante"])

    print("Reposición")
    skus = {"SKU-ejemplo": {"disponible": 18, "en_orden": 10, "reservado": 5, "minimo": 30, "objetivo": 50},
            "SKU-holgado": {"disponible": 80, "en_orden": 0, "reservado": 10, "minimo": 30, "objetivo": 60},
            "SKU-limite": {"disponible": 30, "en_orden": 0, "reservado": 0, "minimo": 30, "objetivo": 45}}
    rep = sugerir_reposicion(skus)
    for sku, v in rep.items():
        print("  ", sku, v)
    #segunda corrida: la orden de 27 ya está abierta, no debe duplicarse
    skus["SKU-ejemplo"]["en_orden"] += rep["SKU-ejemplo"]["sugerencia"]
    rep2 = sugerir_reposicion(skus)
    print("   segunda corrida SKU-ejemplo:", rep2["SKU-ejemplo"])

    for desc, f in [("cantidad negativa", lambda: reservar_fefo(lotes, -3, hoy)),
                    ("disponible negativo", lambda: reservar_fefo([("L-1", date(2027, 1, 1), -5)], 1, hoy)),
                    ("objetivo < mínimo", lambda: sugerir_reposicion({"X": {"disponible": 1, "en_orden": 0, "reservado": 0, "minimo": 10, "objetivo": 5}}))]:
        try:
            f()
        except ValueError as e:
            print(f"   {desc}: error controlado -> {e}")

    assert r1["plan"] == [("L-101", "2026-12-05", 10), ("L-103", "2026-12-05", 15), ("L-104", "2026-12-20", 5)]
    assert r2["faltante"] == 15 and r3["plan"] == [] and r4["faltante"] == 5
    assert rep["SKU-ejemplo"] == {"posicion": 23, "sugerencia": 27}
    assert rep["SKU-holgado"]["sugerencia"] == 0 and rep["SKU-limite"]["sugerencia"] == 15
    assert rep2["SKU-ejemplo"]["sugerencia"] == 0
    print("todas las pruebas pasaron")
