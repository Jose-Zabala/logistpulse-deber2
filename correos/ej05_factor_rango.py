#ejercicio 5 · n2 · ¿tiene n un divisor d con 2 <= d <= b?
#clase: NP · algoritmo: prueba por división exhaustiva + verificador separado

#lectura: valida enteros
def validar(N, B):
    if not isinstance(N, int) or not isinstance(B, int):
        raise ValueError("N y B deben ser enteros")
    if N < 2 or B < 2:
        raise ValueError("se requiere N >= 2 y B >= 2")

#búsqueda: prueba d = 2, 3, ..., min(B, N-1); hasta B-1 divisiones
def buscar_divisor(N, B):
    validar(N, B)
    for d in range(2, min(B, N - 1) + 1):   #d = N no cuenta como divisor propio
        if N % d == 0:
            return d                         #certificado
    return None

#verificador: una comparación y una división, polinomial en los bits de n
def verificar_divisor(N, B, d):
    return isinstance(d, int) and 2 <= d <= B and d < N and N % d == 0

#presentación y pruebas
if __name__ == "__main__":
    N, B = 91, 10
    d = buscar_divisor(N, B)
    print(f"N = {N} ({bin(N)[2:]}, {N.bit_length()} bits), B = {B} ({B.bit_length()} bits)")
    print("divisor encontrado:", d, "| verificación:", verificar_divisor(N, B, d))
    #certificado falso
    print("certificado d = 3:", verificar_divisor(N, B, 3))
    #caso no: 97 es primo
    print("N = 97, B = 10:", buscar_divisor(97, 10))
    #caso límite: 91 = 7 · 13, con b = 6 ningún factor cae en el intervalo
    print("N = 91, B = 6:", buscar_divisor(91, 6))
    #caso inválido
    try:
        buscar_divisor(91, 1)
    except ValueError as e:
        print("error controlado:", e)

    assert d == 7 and verificar_divisor(N, B, d)
    assert buscar_divisor(97, 10) is None and buscar_divisor(91, 6) is None
    print("todas las pruebas pasaron")
