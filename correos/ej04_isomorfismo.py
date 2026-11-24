#ejercicio 4 · n1 · ¿existe isomorfismo entre dos redes?
#clase: NP · algoritmo: búsqueda exhaustiva de permutaciones + verificador
from itertools import permutations

#lectura: valida que sea matriz de adyacencia cuadrada, simétrica, 0/1 y sin lazos
def validar_matriz(M):
    n = len(M)
    for i in range(n):
        if len(M[i]) != n:
            raise ValueError("la matriz no es cuadrada")
        if M[i][i] != 0:
            raise ValueError("no se permiten lazos")
        for j in range(n):
            if M[i][j] not in (0, 1) or M[i][j] != M[j][i]:
                raise ValueError("la matriz debe ser 0/1 y simétrica")

#verificador del certificado: p es biyección y preserva toda adyacencia, o(n^2)
def verificar_isomorfismo(A, B, p):
    n = len(A)
    if len(B) != n or sorted(p) != list(range(n)):
        return False
    return all(A[i][j] == B[p[i]][p[j]] for i in range(n) for j in range(n))

#búsqueda: descarta rápido por número de aristas y grados; luego prueba las n! biyecciones
def buscar_isomorfismo(A, B):
    validar_matriz(A); validar_matriz(B)
    if len(A) != len(B):
        return None
    if sorted(map(sum, A)) != sorted(map(sum, B)):
        return None                     #invariante: secuencias de grados distintas
    for p in permutations(range(len(A))):
        if verificar_isomorfismo(A, B, p):
            return p                    #certificado para la respuesta sí
    return None

#presentación y pruebas
if __name__ == "__main__":
    #red a: camino 0-1-2 ; red b: 1-0-2 (mismo camino con otros nombres)
    A = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    B = [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
    p = buscar_isomorfismo(A, B)
    print("certificado:", p, "| nodo i de A -> nodo p[i] de B")
    print("verificación independiente:", verificar_isomorfismo(A, B, p))
    #certificado falso
    print("certificado identidad:", verificar_isomorfismo(A, B, (0, 1, 2)))
    #caso no isomorfo: triángulo vs camino (3 aristas vs 2)
    T = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
    print("triángulo vs camino:", buscar_isomorfismo(T, A))
    #caso límite: grafo vacío de 0 nodos
    print("grafos vacíos:", buscar_isomorfismo([], []))
    #caso inválido: matriz no simétrica
    try:
        buscar_isomorfismo([[0, 1], [0, 0]], [[0, 1], [1, 0]])
    except ValueError as e:
        print("error controlado:", e)

    assert p is not None and verificar_isomorfismo(A, B, p)
    assert buscar_isomorfismo(T, A) is None
    print("todas las pruebas pasaron")
