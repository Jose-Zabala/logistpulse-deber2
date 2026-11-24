#ejercicio 10 · c3 · ¿bastan k zonas para cubrir todos los corredores? (vertex cover)
#clase: NP-completo · algoritmo: backtracking por ramificación sobre aristas + verificador

#lectura: lista de corredores (u, v) no dirigidos
def validar(corredores, k):
    if not isinstance(k, int) or k < 0:
        raise ValueError("k debe ser un entero no negativo")
    for c in corredores:
        if len(c) != 2 or c[0] == c[1]:
            raise ValueError(f"corredor inválido: {c}")

#verificador: |s| <= k y cada corredor tiene al menos un extremo en s, o(v + e)
def verificar_cobertura(corredores, k, seleccion):
    s = set(seleccion)
    return len(s) <= k and all(u in s or v in s for u, v in corredores)

#búsqueda: toma un corredor sin cubrir (u, v); toda cobertura contiene u o v -> dos ramas
#el árbol tiene profundidad <= k, por eso hay como máximo 2^k hojas
def buscar_cobertura(corredores, k):
    validar(corredores, k)

    def ramificar(pendientes, k_rest, elegidos):
        if not pendientes:
            return elegidos             #todos los corredores cubiertos
        if k_rest == 0:
            return None                 #quedan corredores y no hay equipos
        u, v = pendientes[0]
        for x in (u, v):
            resto = [(a, b) for a, b in pendientes if a != x and b != x]
            r = ramificar(resto, k_rest - 1, elegidos | {x})
            if r is not None:
                return r
        return None
    return ramificar(list(corredores), k, frozenset())

#presentación y pruebas
if __name__ == "__main__":
    corredores = [("A", "B"), ("B", "C")]
    s = buscar_cobertura(corredores, 1)
    print("k = 1 ->", set(s), "| verificación:", verificar_cobertura(corredores, 1, s))
    #caso no: k = 0
    print("k = 0 ->", buscar_cobertura(corredores, 0))
    #triángulo: requiere 2 zonas
    tri = [("A", "B"), ("B", "C"), ("A", "C")]
    print("triángulo k = 1 ->", buscar_cobertura(tri, 1), "| k = 2 ->", set(buscar_cobertura(tri, 2)))
    #red mayor: 6 zonas
    red = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E"), ("E", "F")]
    print("red 6 zonas k = 3 ->", set(buscar_cobertura(red, 3)), "| k = 2 ->", buscar_cobertura(red, 2))
    #certificado falso
    print("certificado {A}:", verificar_cobertura(corredores, 1, {"A"}))
    #caso límite: sin corredores, k = 0 basta
    print("sin corredores ->", set(buscar_cobertura([], 0)))
    #caso inválido
    try:
        buscar_cobertura(corredores, -1)
    except ValueError as e:
        print("error controlado:", e)

    assert s == {"B"} and verificar_cobertura(corredores, 1, s)
    assert buscar_cobertura(tri, 1) is None and verificar_cobertura(tri, 2, buscar_cobertura(tri, 2))
    assert buscar_cobertura(red, 2) is None and verificar_cobertura(red, 3, buscar_cobertura(red, 3))
    print("todas las pruebas pasaron")
