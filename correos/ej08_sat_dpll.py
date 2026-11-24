#ejercicio 8 · c1 · ¿hay una asignación verdadero/falso que cumpla todas las reglas? (3-sat)
#clase: NP-completo · algoritmo: dpll (retroceso con propagación unitaria) + verificador
from itertools import product

#lectura: cláusulas como listas de enteros (k = xk, -k = no xk)
def validar(clausulas, n):
    for c in clausulas:
        if not c:
            raise ValueError("cláusula vacía")
        for lit in c:
            if not isinstance(lit, int) or lit == 0 or abs(lit) > n:
                raise ValueError(f"literal inválido: {lit}")

#verificador: recorre cada literal una vez, o(n + m·k)
def verificar(clausulas, asignacion):
    return all(any(asignacion[abs(l)] == (l > 0) for l in c) for c in clausulas)

#simplifica las cláusulas al fijar un literal como verdadero
def asignar(clausulas, lit):
    nuevas = []
    for c in clausulas:
        if lit in c:
            continue                    #cláusula ya satisfecha
        resto = [l for l in c if l != -lit]
        if not resto:
            return None                 #conflicto: cláusula vacía
        nuevas.append(resto)
    return nuevas

#dpll: propagación unitaria + ramificación sobre una variable; devuelve asignación o none
def dpll(clausulas, asignacion, stats):
    stats["nodos"] += 1
    while True:                         #propagación unitaria
        unitarias = [c[0] for c in clausulas if len(c) == 1]
        if not unitarias:
            break
        lit = unitarias[0]
        asignacion[abs(lit)] = lit > 0
        clausulas = asignar(clausulas, lit)
        if clausulas is None:
            return None
    if not clausulas:
        return asignacion               #todas satisfechas
    var = abs(clausulas[0][0])          #se ramifica sobre la primera variable libre
    for valor in (var, -var):
        nuevas = asignar(clausulas, valor)
        if nuevas is not None:
            a = dict(asignacion); a[var] = valor > 0
            r = dpll(nuevas, a, stats)
            if r is not None:
                return r
    return None                         #ambas ramas fallan: retroceso

def resolver_sat(clausulas, n):
    validar(clausulas, n)
    stats = {"nodos": 0}
    a = dpll([list(c) for c in clausulas], {}, stats)
    if a is not None:
        for v in range(1, n + 1):
            a.setdefault(v, False)      #variables libres: cualquier valor sirve
    return a, stats["nodos"]

#fuerza bruta para comparar: 2^n asignaciones
def sat_fuerza_bruta(clausulas, n):
    for bits in product([False, True], repeat=n):
        a = {i + 1: bits[i] for i in range(n)}
        if verificar(clausulas, a):
            return a
    return None

#presentación y pruebas
if __name__ == "__main__":
    #x1 camión a en franja 1, x2 camión a en franja 2, x3 camión b en franja 1, x4 carga refrigerada en a
    reglas = [[1, 2, 3],      #algún camión cubre una franja
              [-1, -3, 4],    #a y b no pueden compartir la franja 1 sin refrigeración en a
              [-2, -4, 3],    #si a va en franja 2 con refrigeración, b toma franja 1
              [-1, -2, -4],   #a no ocupa dos franjas con carga refrigerada
              [1, -2, 4]]     #a en franja 2 exige franja 1 o refrigeración
    a, nodos = resolver_sat(reglas, 4)
    print("asignación:", dict(sorted(a.items())), "| nodos dpll:", nodos)
    print("verificación independiente:", verificar(reglas, a))

    #cláusulas del expediente (x1 ∨ ¬x2)(x2 ∨ x3)
    exp, _ = resolver_sat([[1, -2], [2, 3]], 3)
    print("expediente:", exp, verificar([[1, -2], [2, 3]], exp))

    #caso no satisfacible: las 8 cláusulas posibles sobre x1, x2, x3
    todas = [[s1 * 1, s2 * 2, s3 * 3] for s1, s2, s3 in product([1, -1], repeat=3)]
    print("8 cláusulas:", resolver_sat(todas, 3)[0], "| fuerza bruta:", sat_fuerza_bruta(todas, 3))
    #caso inválido
    try:
        resolver_sat([[1, 0]], 2)
    except ValueError as e:
        print("error controlado:", e)

    assert a is not None and verificar(reglas, a)
    assert resolver_sat(todas, 3)[0] is None and sat_fuerza_bruta(todas, 3) is None
    #dpll y fuerza bruta deben coincidir en sí/no
    assert (resolver_sat(reglas, 4)[0] is None) == (sat_fuerza_bruta(reglas, 4) is None)
    print("todas las pruebas pasaron")
