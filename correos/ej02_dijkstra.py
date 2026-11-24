#ejercicio 2 · p2 · ruta de menor tiempo desde cd quito hasta cd guayaquil
#clase: P · algoritmo: dijkstra con cola de prioridad (heap)
import heapq

#lectura: lista (origen, destino, tiempo) -> lista de adyacencia; valida pesos no negativos
def construir_grafo(tramos):
    grafo = {}
    for u, v, peso in tramos:
        if peso < 0:
            #dijkstra fija la distancia de un nodo al sacarlo del heap; un peso negativo
            #podría mejorarla después y la respuesta sería incorrecta (usar bellman-ford)
            raise ValueError(f"peso negativo en {u}->{v}: dijkstra no aplica")
        grafo.setdefault(u, []).append((v, peso))
        grafo.setdefault(v, [])
    return grafo

#procesamiento: distancias mínimas desde el origen y predecesores
def dijkstra(grafo, origen):
    if origen not in grafo:
        raise ValueError("origen no existe")
    dist = {v: float("inf") for v in grafo}
    previo = {v: None for v in grafo}   #información necesaria para reconstruir la ruta
    dist[origen] = 0
    heap = [(0, origen)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue                    #entrada vieja del heap, se ignora
        for v, peso in grafo[u]:
            nd = d + peso
            if nd < dist[v]:            #relajación de la arista
                dist[v] = nd
                previo[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, previo

#reconstruye la ruta siguiendo predecesores desde el destino
def reconstruir(previo, dist, destino):
    if dist[destino] == float("inf"):
        return None
    ruta = []
    while destino is not None:
        ruta.append(destino)
        destino = previo[destino]
    return ruta[::-1]

#verificador: una ruta propuesta existe en el grafo y su costo es el indicado
def costo_ruta(grafo, ruta):
    total = 0
    for u, v in zip(ruta, ruta[1:]):
        pesos = [p for w, p in grafo[u] if w == v]
        if not pesos:
            return None
        total += min(pesos)
    return total

#presentación y pruebas
if __name__ == "__main__":
    tramos = [("Quito", "Latacunga", 2), ("Quito", "Ambato", 5),
              ("Latacunga", "Guayaquil", 6), ("Ambato", "Guayaquil", 3)]
    g = construir_grafo(tramos)
    dist, previo = dijkstra(g, "Quito")
    ruta = reconstruir(previo, dist, "Guayaquil")
    print("distancias:", dist)
    print("ruta sugerida:", " -> ".join(ruta), "| tiempo:", dist["Guayaquil"])
    #empate: quito-ambato-guayaquil también cuesta 8; dijkstra conserva la primera encontrada
    print("costo ruta alterna por ambato:", costo_ruta(g, ["Quito", "Ambato", "Guayaquil"]))

    #caso límite: nodo sin salida, no alcanza a quito
    dist_g, previo_g = dijkstra(g, "Guayaquil")
    print("Guayaquil -> Quito:", reconstruir(previo_g, dist_g, "Quito"))
    #caso inválido: peso negativo
    try:
        construir_grafo([("A", "B", 4), ("B", "C", -2)])
    except ValueError as e:
        print("error controlado:", e)

    assert dist["Guayaquil"] == 8 and ruta == ["Quito", "Latacunga", "Guayaquil"]
    assert costo_ruta(g, ruta) == dist["Guayaquil"]
    print("todas las pruebas pasaron")
