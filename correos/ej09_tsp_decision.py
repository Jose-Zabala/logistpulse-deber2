#ejercicio 9 · c2 · ¿existe un recorrido que visite cada centro una vez y regrese con costo <= l?
#clase: NP-completo · algoritmo: backtracking (enumerar permutaciones con poda) + verificador
from itertools import permutations

#lectura: matriz cuadrada de distancias no negativas
def validar(dist, limite):
    n = len(dist)
    if n < 2 or any(len(f) != n for f in dist):
        raise ValueError("matriz de distancias inválida")
    if any(d < 0 for f in dist for d in f) or limite < 0:
        raise ValueError("distancias y límite deben ser no negativos")

#verificador: el recorrido es permutación de todos los centros, cierra en el origen y cuesta <= l, o(n)
def verificar_recorrido(dist, limite, recorrido):
    n = len(dist)
    if len(recorrido) != n + 1 or recorrido[0] != recorrido[-1]:
        return False
    if sorted(recorrido[:-1]) != list(range(n)):
        return False
    costo = sum(dist[recorrido[i]][recorrido[i + 1]] for i in range(n))
    return costo <= limite

#decisión: backtracking que corta una rama apenas su costo parcial supera l
def existe_recorrido(dist, limite):
    validar(dist, limite)
    n = len(dist)
    camino, usados = [0], {0}

    def extender(costo):
        if costo > limite:
            return None                 #poda
        if len(camino) == n:
            total = costo + dist[camino[-1]][0]
            return (camino + [0], total) if total <= limite else None
        for v in range(1, n):
            if v not in usados:
                camino.append(v); usados.add(v)
                r = extender(costo + dist[camino[-2]][v])
                camino.pop(); usados.discard(v)
                if r:
                    return r
        return None
    return extender(0)                  #devuelve (recorrido, costo) o none

#optimización (otra pregunta): recorrido de menor costo probando las (n-1)! rutas
def recorrido_minimo(dist):
    n = len(dist)
    mejor = None
    for perm in permutations(range(1, n)):
        r = (0,) + perm + (0,)
        c = sum(dist[r[i]][r[i + 1]] for i in range(n))
        if mejor is None or c < mejor[1]:
            mejor = (list(r), c)
    return mejor

#presentación y pruebas
if __name__ == "__main__":
    centros = ["Planta", "Quito", "Guayaquil"]
    d = [[0, 4, 8], [4, 0, 3], [8, 3, 0]]
    L = 20
    r = existe_recorrido(d, L)
    print(f"L = {L}: sí ->", [centros[i] for i in r[0]], "| costo", r[1])
    print("verificación:", verificar_recorrido(d, L, r[0]))
    print("óptimo (pregunta de optimización):", recorrido_minimo(d))
    #caso no: l menor que el óptimo
    print("L = 14:", existe_recorrido(d, 14))
    #caso con 5 centros
    d5 = [[0, 2, 9, 10, 7], [2, 0, 6, 4, 3], [9, 6, 0, 8, 5], [10, 4, 8, 0, 6], [7, 3, 5, 6, 0]]
    print("5 centros, L = 26:", existe_recorrido(d5, 26), "| L = 25:", existe_recorrido(d5, 25))
    print("5 centros, óptimo:", recorrido_minimo(d5))
    #certificado inválido: repite un centro
    print("certificado [0,1,1,0]:", verificar_recorrido(d, L, [0, 1, 1, 0]))
    #caso inválido
    try:
        existe_recorrido([[0, -1], [-1, 0]], 5)
    except ValueError as e:
        print("error controlado:", e)

    assert r is not None and r[1] == 15 and verificar_recorrido(d, L, r[0])
    assert existe_recorrido(d, 14) is None
    #la decisión debe coincidir con comparar el óptimo contra l
    assert (existe_recorrido(d5, 25) is not None) == (recorrido_minimo(d5)[1] <= 25)
    print("todas las pruebas pasaron")
