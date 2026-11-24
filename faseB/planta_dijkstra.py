#fase b · ruta del amr en la planta con dijkstra
#grafo no dirigido (los pasillos se recorren en ambos sentidos), pesos en metros, todos no negativos
import heapq

#lectura: zonas y pasillos de la figura 5
ZONAS = {"R": "Recepción", "A": "Pasillo A", "B": "Pasillo B", "C": "Pasillo C",
         "P": "Picking", "E": "Empaque", "D": "Despacho"}
PASILLOS = [("R", "A", 4), ("R", "B", 2), ("A", "B", 1), ("A", "P", 3), ("A", "E", 5),
            ("B", "P", 7), ("B", "C", 3), ("P", "E", 2), ("P", "C", 2), ("C", "E", 4), ("E", "D", 3)]

#construye la lista de adyacencia omitiendo zonas bloqueadas; valida pesos y zonas
def construir_grafo(zonas, pasillos, bloqueadas=()):
    for z in bloqueadas:
        if z not in zonas:
            raise ValueError(f"zona bloqueada desconocida: {z}")
    grafo = {z: [] for z in zonas if z not in bloqueadas}
    for u, v, w in pasillos:
        if u not in zonas or v not in zonas:
            raise ValueError(f"pasillo con zona desconocida: {u}-{v}")
        if w < 0:
            raise ValueError(f"distancia negativa en {u}-{v}: dijkstra no aplica")
        if u in grafo and v in grafo:
            grafo[u].append((v, w))
            grafo[v].append((u, w))     #no dirigido: se agregan ambos sentidos
    return grafo

#procesamiento: dijkstra con heap; guarda todos los predecesores que empatan en distancia mínima
def dijkstra(grafo, origen):
    if origen not in grafo:
        raise ValueError(f"origen {origen} no existe o está bloqueado")
    dist = {v: float("inf") for v in grafo}
    pred = {v: [] for v in grafo}
    dist[origen] = 0
    heap = [(0, origen)]
    visitados = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in visitados:
            continue                    #entrada vieja del heap
        visitados.add(u)                #con pesos >= 0, dist[u] ya es definitiva
        for v, w in grafo[u]:
            nd = d + w
            if nd < dist[v]:            #mejora estricta: nuevo predecesor único
                dist[v] = nd
                pred[v] = [u]
                heapq.heappush(heap, (nd, v))
            elif nd == dist[v] and u not in pred[v]:
                pred[v].append(u)       #empate: otra ruta óptima
    return dist, pred

#reconstruye todas las rutas óptimas siguiendo predecesores desde el destino
def rutas_optimas(pred, dist, origen, destino):
    if destino not in dist or dist[destino] == float("inf"):
        return []
    if destino == origen:
        return [[origen]]
    rutas = []
    for p in pred[destino]:
        for r in rutas_optimas(pred, dist, origen, p):
            rutas.append(r + [destino])
    return rutas

#verificador: la ruta usa pasillos existentes y devuelve su costo
def costo_ruta(grafo, ruta):
    total = 0
    for u, v in zip(ruta, ruta[1:]):
        w = [p for x, p in grafo.get(u, []) if x == v]
        if not w:
            return None
        total += w[0]
    return total

#presentación
def reportar(titulo, grafo, origen, destino):
    dist, pred = dijkstra(grafo, origen)
    rutas = rutas_optimas(pred, dist, origen, destino)
    print(f"\n{titulo}")
    if not rutas:
        print(f"  no existe ruta de {origen} a {destino}")
    for r in rutas:
        print(f"  {' -> '.join(r)} | {costo_ruta(grafo, r)} m")
    return dist, rutas

if __name__ == "__main__":
    g = construir_grafo(ZONAS, PASILLOS)
    dist, rutas = reportar("escenario base: AMR de R (Recepción) a D (Despacho), sin bloqueos", g, "R", "D")
    print("  distancias desde R:", dist)
    #ruta de la figura 5
    figura = ["R", "B", "A", "P", "E", "D"]
    print("  ruta de la figura 5:", costo_ruta(g, figura), "m")

    #caso normal: pasillo a bloqueado
    reportar("pasillo A bloqueado", construir_grafo(ZONAS, PASILLOS, {"A"}), "R", "D")
    #caso límite: empaque bloqueado deja despacho aislado
    reportar("empaque bloqueado", construir_grafo(ZONAS, PASILLOS, {"E"}), "R", "D")
    #caso límite: origen = destino
    reportar("origen igual a destino", g, "R", "R")
    #casos inválidos
    for desc, f in [("distancia negativa", lambda: construir_grafo(ZONAS, [("R", "A", -4)])),
                    ("zona inexistente", lambda: construir_grafo(ZONAS, PASILLOS, {"Z"})),
                    ("origen bloqueado", lambda: dijkstra(construir_grafo(ZONAS, PASILLOS, {"R"}), "R"))]:
        try:
            f()
        except ValueError as e:
            print(f"\n{desc}: error controlado -> {e}")

    assert dist["D"] == 11 and figura in rutas and costo_ruta(g, figura) == 11
    assert len(rutas) == 2
    assert dijkstra(construir_grafo(ZONAS, PASILLOS, {"A"}), "R")[0]["D"] == 12
    dist_e, pred_e = dijkstra(construir_grafo(ZONAS, PASILLOS, {"E"}), "R")
    assert dist_e["D"] == float("inf") and rutas_optimas(pred_e, dist_e, "R", "D") == []
    print("\ntodas las pruebas pasaron")
