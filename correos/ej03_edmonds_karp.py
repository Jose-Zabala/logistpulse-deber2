#ejercicio 3 · p3 · máximo de camiones por día desde planta hasta clientes
#clase: P · algoritmo: edmonds-karp (ford-fulkerson con bfs)
from collections import deque

#lectura: lista (origen, destino, capacidad) -> capacidades residuales
def construir_residual(tramos):
    residual = {}
    for u, v, c in tramos:
        if not isinstance(c, int) or c < 0:
            raise ValueError(f"capacidad inválida en {u}->{v}: {c}")
        residual.setdefault(u, {}).setdefault(v, 0)
        residual.setdefault(v, {}).setdefault(u, 0)   #arista inversa con capacidad 0
        residual[u][v] += c
    return residual

#bfs sobre el grafo residual: devuelve padres si encuentra un camino aumentante
def bfs_camino(residual, s, t):
    padre = {s: None}
    cola = deque([s])
    while cola:
        u = cola.popleft()
        for v, c in residual[u].items():
            if c > 0 and v not in padre:
                padre[v] = u
                if v == t:
                    return padre
                cola.append(v)
    return None

#procesamiento: repite bfs + cuello de botella hasta que no haya camino aumentante
def edmonds_karp(tramos, s, t):
    residual = construir_residual(tramos)
    if s not in residual or t not in residual:
        raise ValueError("fuente o sumidero no existe")
    if s == t:
        raise ValueError("fuente y sumidero deben ser distintos")
    flujo_total = 0
    registro = []                       #registro reproducible de cada aumento
    while True:
        padre = bfs_camino(residual, s, t)
        if padre is None:
            break                       #no hay camino aumentante: el flujo es máximo
        camino = [t]
        while camino[-1] != s:
            camino.append(padre[camino[-1]])
        camino.reverse()
        cuello = min(residual[u][v] for u, v in zip(camino, camino[1:]))
        for u, v in zip(camino, camino[1:]):
            residual[u][v] -= cuello    #se usa capacidad en el sentido directo
            residual[v][u] += cuello    #se habilita deshacer en el sentido inverso
        flujo_total += cuello
        registro.append((camino, cuello, flujo_total))
    #flujo por tramo = capacidad original - residual final
    flujo_tramo = {(u, v): c - residual[u][v] for u, v, c in tramos}
    return flujo_total, flujo_tramo, registro

#verificador: el flujo respeta capacidades y conservación en nodos intermedios
def verificar_flujo(tramos, flujo_tramo, s, t):
    balance = {}
    for u, v, c in tramos:
        f = flujo_tramo[(u, v)]
        if f < 0 or f > c:
            return False
        balance[u] = balance.get(u, 0) - f
        balance[v] = balance.get(v, 0) + f
    return all(b == 0 for n, b in balance.items() if n not in (s, t))

#presentación y pruebas
if __name__ == "__main__":
    tramos = [("Planta", "Quito", 7), ("Planta", "Guayaquil", 5), ("Quito", "Clientes", 4),
              ("Guayaquil", "Clientes", 6), ("Quito", "Guayaquil", 2)]
    total, por_tramo, registro = edmonds_karp(tramos, "Planta", "Clientes")
    for i, (camino, cuello, acumulado) in enumerate(registro, 1):
        print(f"aumento {i}: {' -> '.join(camino)} | +{cuello} | acumulado {acumulado}")
    print("flujo por tramo:", por_tramo)
    print("flujo máximo:", total, "camiones/día")
    print("suma de salida de planta:", 7 + 5, "(no es lo que llega: el corte hacia clientes es 4 + 6 = 10)")

    #caso límite: sin camino de planta a clientes
    total_0, _, _ = edmonds_karp([("Planta", "Quito", 7), ("Clientes", "Quito", 3)], "Planta", "Clientes")
    print("sin camino:", total_0)
    #caso inválido: capacidad negativa
    try:
        edmonds_karp([("Planta", "Quito", -1)], "Planta", "Quito")
    except ValueError as e:
        print("error controlado:", e)

    assert total == 10 and verificar_flujo(tramos, por_tramo, "Planta", "Clientes")
    assert total_0 == 0
    print("todas las pruebas pasaron")
