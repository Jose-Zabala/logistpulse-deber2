#ejercicio 1 · p1 · ¿existe un camino desde planta durán hasta zona norte?
#clase: P · algoritmo: bfs (búsqueda en anchura)
from collections import deque

#lectura: sitios y tramos activos (origen, destino) -> lista de adyacencia dirigida
def construir_grafo(tramos, sitios=()):
    grafo = {s: [] for s in sitios}     #un sitio puede quedar aislado por un cierre
    for tramo in tramos:
        if len(tramo) != 2:
            raise ValueError(f"tramo inválido: {tramo}")
        u, v = tramo
        grafo.setdefault(u, []).append(v)
        grafo.setdefault(v, [])  #asegura que el destino exista como vértice
    return grafo

#procesamiento: bfs que guarda el padre de cada vértice para reconstruir la ruta
def buscar_ruta(grafo, origen, destino):
    if origen not in grafo or destino not in grafo:
        raise ValueError("origen o destino no existe en la red")
    padre = {origen: None}          #también funciona como conjunto de visitados
    cola = deque([origen])
    while cola:                     #termina: cada vértice entra a la cola una sola vez
        actual = cola.popleft()
        if actual == destino:
            ruta = []
            while actual is not None:   #se reconstruye el camino con los padres
                ruta.append(actual)
                actual = padre[actual]
            return ruta[::-1]
        for vecino in grafo[actual]:
            if vecino not in padre:
                padre[vecino] = actual
                cola.append(vecino)
    return None                     #cola agotada: no existe camino

#decisión sí/no a partir de la búsqueda
def alcanzable(grafo, origen, destino):
    return buscar_ruta(grafo, origen, destino) is not None

#presentación y pruebas
if __name__ == "__main__":
    tramos = [("Durán", "Quito"), ("Durán", "Guayaquil"), ("Quito", "Norte"), ("Guayaquil", "Sur")]
    sitios = ["Durán", "Quito", "Guayaquil", "Norte", "Sur"]
    red = construir_grafo(tramos, sitios)

    #caso normal alcanzable
    print("Durán -> Norte:", alcanzable(red, "Durán", "Norte"), buscar_ruta(red, "Durán", "Norte"))
    #caso normal no alcanzable (las rutas son dirigidas)
    print("Sur -> Norte:", alcanzable(red, "Sur", "Norte"))
    #caso con cierre de vía: se elimina quito -> norte
    red_cierre = construir_grafo([t for t in tramos if t != ("Quito", "Norte")], sitios)
    print("Durán -> Norte con cierre:", alcanzable(red_cierre, "Durán", "Norte"))
    #caso límite: origen igual a destino
    print("Durán -> Durán:", buscar_ruta(red, "Durán", "Durán"))
    #caso inválido: nodo inexistente
    try:
        alcanzable(red, "Durán", "Cuenca")
    except ValueError as e:
        print("error controlado:", e)

    assert buscar_ruta(red, "Durán", "Norte") == ["Durán", "Quito", "Norte"]
    assert not alcanzable(red, "Sur", "Norte")
    assert not alcanzable(red_cierre, "Durán", "Norte")
    print("todas las pruebas pasaron")
