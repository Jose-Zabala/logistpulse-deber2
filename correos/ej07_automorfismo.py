#ejercicio 7 · n4 · ¿el grafo tiene un automorfismo distinto de la identidad?
#clase: NP · algoritmo: permutaciones + verificación de adyacencia
from itertools import permutations

#lectura: matriz de adyacencia cuadrada, simétrica, 0/1 y sin lazos
def validar_matriz(A):
    n = len(A)
    for i in range(n):
        if len(A[i]) != n or A[i][i] != 0:
            raise ValueError("matriz no cuadrada o con lazos")
        for j in range(n):
            if A[i][j] not in (0, 1) or A[i][j] != A[j][i]:
                raise ValueError("la matriz debe ser 0/1 y simétrica")

#verificador independiente: p es permutación, no es identidad y preserva adyacencias, o(n^2)
def verificar_automorfismo(A, p):
    n = len(A)
    if sorted(p) != list(range(n)) or tuple(p) == tuple(range(n)):
        return False
    return all(A[i][j] == A[p[i]][p[j]] for i in range(n) for j in range(n))

#búsqueda: prueba las n! - 1 permutaciones; solo cruza vértices de igual grado
def buscar_automorfismo(A):
    validar_matriz(A)
    n = len(A)
    grado = [sum(fila) for fila in A]
    for p in permutations(range(n)):
        if any(grado[i] != grado[p[i]] for i in range(n)):
            continue                    #poda: un automorfismo conserva grados
        if verificar_automorfismo(A, p):
            return p                    #certificado
    return None                         #se agotaron todas las permutaciones

#presentación y pruebas
if __name__ == "__main__":
    #triángulo del expediente
    T = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
    p = buscar_automorfismo(T)
    print("triángulo -> certificado:", p, "| verificación:", verificar_automorfismo(T, p))

    #grafo asimétrico de 6 vértices: solo tiene la identidad
    aristas = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 4), (3, 5)]
    G = [[0] * 6 for _ in range(6)]
    for u, v in aristas:
        G[u][v] = G[v][u] = 1
    print("grafo asimétrico:", buscar_automorfismo(G), "(se probaron 720 permutaciones)")
    #certificado falso: la identidad no cuenta
    print("identidad como certificado:", verificar_automorfismo(T, (0, 1, 2)))
    #caso límite: un solo vértice, solo existe la identidad
    print("un vértice:", buscar_automorfismo([[0]]))
    #caso inválido
    try:
        buscar_automorfismo([[1]])
    except ValueError as e:
        print("error controlado:", e)

    assert p == (0, 2, 1) and verificar_automorfismo(T, p)
    assert buscar_automorfismo(G) is None
    print("todas las pruebas pasaron")
