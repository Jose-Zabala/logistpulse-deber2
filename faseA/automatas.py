#fase a · autómatas de pedido, reserva y orden de compra
#cada autómata es un afd m = (q, σ, δ, q0, f); δ es parcial: toda transición no definida
#lleva al estado sumidero implícito q_err y la secuencia se rechaza (igual que en jflap)
import xml.etree.ElementTree as ET
import subprocess, sys

PEDIDO = {
    "nombre": "pedido",
    "estados": ["Borrador", "Confirmado", "Reservado", "Preparacion", "Empacado", "Despachado", "Entregado", "Cancelado"],
    "eventos": {"c": "confirmar", "r": "reservar", "i": "iniciar picking", "e": "empacar",
                "d": "despachar", "t": "entregar", "x": "cancelar / liberar"},
    "inicial": "Borrador",
    "finales": ["Entregado", "Cancelado"],
    "delta": {("Borrador", "c"): "Confirmado", ("Borrador", "x"): "Cancelado",
              ("Confirmado", "r"): "Reservado", ("Confirmado", "x"): "Cancelado",
              ("Reservado", "i"): "Preparacion", ("Reservado", "x"): "Cancelado",
              ("Preparacion", "e"): "Empacado", ("Empacado", "d"): "Despachado",
              ("Despachado", "t"): "Entregado"},
    "pruebas": [("criedt", True, "flujo completo hasta Entregado"),
                ("crx", True, "se libera la reserva y se cancela antes del picking"),
                ("x", True, "borrador cancelado"),
                ("d", False, "Borrador -> Despachado: no existe δ(Borrador, despachar)"),
                ("crid", False, "despachar sin empacar: no existe δ(Preparacion, despachar)"),
                ("criedtx", False, "cancelar un pedido ya entregado: Entregado no tiene salidas"),
                ("crie", False, "termina en Empacado, que no es final")],
}

RESERVA = {
    "nombre": "reserva",
    "estados": ["Solicitada", "Validada", "Reservada", "Consumida", "Liberada", "Expirada", "Rechazada"],
    "eventos": {"v": "validar", "n": "sin stock", "c": "confirmar", "k": "picking",
                "x": "cancelar", "z": "vence plazo"},
    "inicial": "Solicitada",
    "finales": ["Consumida", "Liberada", "Expirada", "Rechazada"],
    "delta": {("Solicitada", "v"): "Validada", ("Solicitada", "n"): "Rechazada",
              ("Validada", "c"): "Reservada",
              ("Reservada", "k"): "Consumida", ("Reservada", "x"): "Liberada", ("Reservada", "z"): "Expirada"},
    "pruebas": [("vck", True, "Solicitada -> Validada -> Reservada -> Consumida"),
                ("vcz", True, "la reserva vence sin consumirse"),
                ("n", True, "se rechaza por falta de stock"),
                ("vk", False, "consumir una reserva nunca confirmada: no existe δ(Validada, picking)"),
                ("k", False, "consumir sin validar ni confirmar"),
                ("nv", False, "validar una solicitud ya rechazada"),
                ("vckx", False, "cancelar una reserva ya consumida")],
}

COMPRA = {
    "nombre": "orden_compra",
    "estados": ["Borrador", "EnAprobacion", "Aprobada", "Enviada", "RecepcionParcial", "Recibida", "Rechazada"],
    "eventos": {"s": "solicitar aprobación", "a": "aprobar", "j": "rechazar", "e": "emitir orden",
                "p": "recibir parte", "k": "recibir completa", "c": "completar recepción"},
    "inicial": "Borrador",
    "finales": ["Recibida", "Rechazada"],
    "delta": {("Borrador", "s"): "EnAprobacion",
              ("EnAprobacion", "a"): "Aprobada", ("EnAprobacion", "j"): "Rechazada",
              ("Aprobada", "e"): "Enviada",
              ("Enviada", "k"): "Recibida", ("Enviada", "p"): "RecepcionParcial",
              ("RecepcionParcial", "p"): "RecepcionParcial",   #completado: varias entregas parciales
              ("RecepcionParcial", "c"): "Recibida"},
    "pruebas": [("saek", True, "aprobada, emitida y recibida completa"),
                ("saeppc", True, "dos recepciones parciales y luego se completa"),
                ("sj", True, "la orden se rechaza en aprobación"),
                ("sje", False, "Rechazada -> Enviada: un estado final rechazado no habilita emisión"),
                ("se", False, "emitir sin aprobar"),
                ("saep", False, "queda en RecepcionParcial, que no es final"),
                ("saekp", False, "recibir partes después de Recibida")],
}

AUTOMATAS = [PEDIDO, RESERVA, COMPRA]

#simulación del afd: devuelve (aceptada, recorrido, motivo)
def simular(m, cadena):
    q = m["inicial"]; recorrido = [q]
    for simbolo in cadena:
        if simbolo not in m["eventos"]:
            return False, recorrido, f"símbolo '{simbolo}' fuera de Σ"
        sig = m["delta"].get((q, simbolo))
        if sig is None:
            return False, recorrido + ["q_err"], f"δ({q}, {m['eventos'][simbolo]}) no definida"
        q = sig; recorrido.append(q)
    if q in m["finales"]:
        return True, recorrido, f"termina en {q} ∈ F"
    return False, recorrido, f"termina en {q} ∉ F"

#posiciones de los estados calculadas con graphviz, para que el .jff se vea como el diagrama
def posiciones(m):
    L = ['digraph g { rankdir=LR; nodesep=0.8; ranksep=1.2;']
    L += [f'"{q}";' for q in m["estados"]]
    L += [f'"{q}" -> "{p}";' for (q, a), p in m["delta"].items()]
    L.append("}")
    salida = subprocess.run(["dot", "-Tplain"], input="\n".join(L), text=True, capture_output=True, check=True).stdout
    pos = {}
    for linea in salida.splitlines():
        t = linea.split()
        if t[0] == "node":
            pos[t[1].strip('"')] = (float(t[2]), float(t[3]))
    max_y = max(y for x, y in pos.values())
    return {q: (60 + x * 85, 60 + (max_y - y) * 85) for q, (x, y) in pos.items()}

#escritura del archivo jflap (.jff)
def escribir_jff(m, ruta):
    raiz = ET.Element("structure"); ET.SubElement(raiz, "type").text = "fa"
    aut = ET.SubElement(raiz, "automaton")
    ids = {q: i for i, q in enumerate(m["estados"])}
    pos = posiciones(m)
    for q, i in ids.items():
        s = ET.SubElement(aut, "state", id=str(i), name=q)
        ET.SubElement(s, "x").text = f"{pos[q][0]:.1f}"; ET.SubElement(s, "y").text = f"{pos[q][1]:.1f}"
        if q == m["inicial"]: ET.SubElement(s, "initial")
        if q in m["finales"]: ET.SubElement(s, "final")
    for (q, a), p in m["delta"].items():
        t = ET.SubElement(aut, "transition")
        ET.SubElement(t, "from").text = str(ids[q]); ET.SubElement(t, "to").text = str(ids[p])
        ET.SubElement(t, "read").text = a
    ET.indent(raiz)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?><!--Created with JFLAP 7.1.-->\n')
        f.write(ET.tostring(raiz, encoding="unicode"))

#lectura del .jff para probar que el archivo entregado acepta y rechaza lo esperado
def leer_jff(ruta, eventos):
    aut = ET.parse(ruta).getroot().find("automaton")
    nombres = {s.get("id"): s.get("name") for s in aut.findall("state")}
    m = {"eventos": eventos, "delta": {}, "finales": []}
    for s in aut.findall("state"):
        if s.find("initial") is not None: m["inicial"] = s.get("name")
        if s.find("final") is not None: m["finales"].append(s.get("name"))
    for t in aut.findall("transition"):
        m["delta"][(nombres[t.findtext("from")], t.findtext("read"))] = nombres[t.findtext("to")]
    return m

#diagrama de estados con graphviz
def escribir_png(m, ruta):
    L = [f'digraph "{m["nombre"]}" {{', 'rankdir=LR; bgcolor=white; node [fontname="Helvetica", style=filled, fillcolor="#eef4fc", color="#7f9cc4"]; edge [fontname="Helvetica", fontsize=11, color="#4f6886"];',
         f'labelloc=t; fontname="Helvetica"; fontsize=20; label="Autómata · {m["nombre"].replace("_", " ")}";',
         'inicio [shape=point, width=0.12];']
    for q in m["estados"]:
        forma = "doublecircle" if q in m["finales"] else "ellipse"
        color = '"#e3f4e8"' if q in ("Entregado", "Consumida", "Recibida") else ('"#fbe9e9"' if q in ("Cancelado", "Rechazada") else '"#eef4fc"')
        L.append(f'"{q}" [shape={forma}, fillcolor={color}];')
    L.append(f'inicio -> "{m["inicial"]}";')
    for (q, a), p in m["delta"].items():
        L.append(f'"{q}" -> "{p}" [label="{a}: {m["eventos"][a]}"];')
    L.append("}")
    subprocess.run(["dot", "-Tpng", "-Gdpi=150", "-o", ruta], input="\n".join(L), text=True, check=True)

if __name__ == "__main__":
    fallas = 0
    for m in AUTOMATAS:
        jff = f"{m['nombre']}.jff"
        escribir_jff(m, jff); escribir_png(m, f"{m['nombre']}.png")
        desde_jff = leer_jff(jff, m["eventos"])
        print(f"\n=== {m['nombre']} ===")
        for cadena, esperado, desc in m["pruebas"]:
            ok, rec, motivo = simular(desde_jff, cadena)
            marca = "OK " if ok == esperado else "FALLA"
            fallas += ok != esperado
            print(f"[{marca}] '{cadena}': {'ACEPTA' if ok else 'RECHAZA'} · {' -> '.join(rec)} · {motivo} · {desc}")
    print("\ntodas las pruebas pasaron" if fallas == 0 else f"\n{fallas} pruebas fallaron")
    sys.exit(1 if fallas else 0)
